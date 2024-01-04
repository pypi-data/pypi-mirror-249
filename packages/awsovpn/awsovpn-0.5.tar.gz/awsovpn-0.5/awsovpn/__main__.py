#!/usr/bin/env python

import argparse
import boto3
import os
import sys
import paramiko
import time
import re
from dotenv import load_dotenv

#--------------------------------------------------------------------------------
# AWS credentials and region configuration
#--------------------------------------------------------------------------------
instance_type = 't2.micro'
key_name = 'AwsVpnKey'
stack_name = 'AwsVpnStack'

#--------------------------------------------------------------------------------
# To find the latest AMI, go to https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#LaunchInstances:
# and search for 'OpenVPN'.
#--------------------------------------------------------------------------------
ami_id = 'ami-0fa9e125394e28eef'
ovpn_user_name='openvpnas'
debug = False


#--------------------------------------------------------------------------------

def create_boto3_session(access_key_id, secret_access_key, profile_name, region_name):
    global session
    session = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        profile_name=profile_name,
        region_name=region_name
    )
    return session

def ensure_session():
    global session
    if 'session' not in globals() or not session:
        print("Error: no valid session.")
        sys.exit(1)
    return session

def ensure_ec2():
    ensure_session()
    global ec2
    if 'ec2' not in globals() or not ec2:
        ec2 = session.client('ec2')
    return ec2

def ensure_cfn():
    ensure_session()
    global cfn
    if 'cfn' not in globals() or not cfn:
        cfn = session.client('cloudformation')
    return cfn


def read_public_key(key_file_name):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    # Load the private key from a file
    with open(key_file_name, 'rb') as private_key_file:
        private_key_data = private_key_file.read()

    # Deserialize the private key
    private_key = serialization.load_pem_private_key(private_key_data, password=None)

    # Extract the public key
    public_key = private_key.public_key()

    # Serialize the public key to OpenSSH format
    public_key_ssh = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )
    return public_key_ssh.decode('utf-8')


def write_private_key(key_file_name, private_key_material):
    # Save the private key to a file
    with open(key_file_name, "w") as key_file:
        key_file.write(private_key_material)
    os.chmod(key_file_name, 0o400)  # Set strict permissions on the private key file



def ensure_key_pair(key_name):
    """Ensure that AWS has a key by the given key_name.  Create a new one if necessary."""
    ensure_ec2()
    # Check if the key file exists.
    key_file_name = f"{key_name}.pem"
    if os.path.isfile(key_file_name):
        # The private key file exists; Make sure that it's public key exists in ec2.
        try:
            ec2.describe_key_pairs(KeyNames=[key_name])
            print(f"Key pair '{key_name}' already exists.")
        except ec2.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "InvalidKeyPair.NotFound":
                # Import public key into ec2
                try:
                    public_key_material = read_public_key(key_file_name)
                    response = ec2.import_key_pair(KeyName=key_name, PublicKeyMaterial=public_key_material)
                    print(f"Key pair '{key_name}' imported successfully.")
                except Exception as e:
                    print(f"Error importing key pair: {e}")

            else:
                print(f"Error checking/creating key pair: {e}")
    
    else:
        # The private key file does not exist; Create a new key pair in ec2 and save the private key to a file
        key_pair = ec2.create_key_pair(KeyName=key_name)
        private_key_material = key_pair["KeyMaterial"]
        write_private_key(key_file_name, private_key_material)
        print(f"Key pair '{key_name}' created, and the private key is saved to {key_file_name}.")
        return True


def ensure_stack(stack_name):
    ensure_cfn()
    try: 
        # Check if stack already exists
        stack = cfn.describe_stacks(StackName=stack_name)['Stacks'][0]
        print(f"Stack {stack_name} already exists.")
    except Exception as e:
        create_stack(stack_name)

        
def create_stack(stack_name):
    ensure_cfn()
    ensure_key_pair(key_name)
    stack_template = """
    Resources:
      EC2Instance:
        Type: AWS::EC2::Instance
        Properties:
          InstanceType: {}
          KeyName: {}
          SecurityGroupIds:
            - !Ref VPNSecurityGroup
          ImageId: {}
      VPNSecurityGroup:
        Type: AWS::EC2::SecurityGroup
        Properties:
          GroupDescription: OpenVPN Security Group
          SecurityGroupIngress:
            - CidrIp: 0.0.0.0/0
              FromPort: 22     # SSH
              ToPort: 22
              IpProtocol: tcp
            - CidrIp: 0.0.0.0/0
              FromPort: 443    # Web interface (HTTPS)
              ToPort: 443
              IpProtocol: tcp
            - CidrIp: 0.0.0.0/0
              FromPort: 953    # Clustering (TCP)
              ToPort: 953
              IpProtocol: tcp
            - CidrIp: 0.0.0.0/0
              FromPort: 1194   # OpenVPN (UDP)
              ToPort: 1194
              IpProtocol: udp
            - CidrIp: 0.0.0.0/0
              FromPort: 943    # Web interface (TCP)
              ToPort: 943
              IpProtocol: tcp
    Outputs:
      EC2InstanceId:
        Description: EC2 Instance ID
        Value: !Ref EC2Instance
    """.format(instance_type, key_name, ami_id)

    cfn.create_stack(
        StackName=stack_name,
        TemplateBody=stack_template,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )

def wait_for_stack(stack_name, target_status = ['CREATE_COMPLETE', 'ROLLBACK_COMPLETE']):
    if isinstance(target_status, str):
        target_status = [target_status]
    ensure_cfn()
    while True:
        stack = cfn.describe_stacks(StackName=stack_name)['Stacks'][0]
        stack_status = stack['StackStatus']
        if stack_status in target_status:
            break
        print(f"Waiting for Stack...  Stack status: {stack_status}")
        time.sleep(10)


def wait_for_ssh(hostname, port=22, username=None, password=None, key_filename=None):
    start_time = time.time()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    success = False
    attempts = 0

    while True:
        try:
            ssh_client.connect(
                hostname=hostname,
                port=port,
                username=username,
                password=password,
                key_filename=key_filename,
            )
            if debug:
                print("SSH service is active.")
            ssh_client.close()
            success = True
            break
        except paramiko.ssh_exception.SSHException as e:
            if "Connection refused" in str(e):
                print("SSH service is not yet active. Retrying in 10 seconds...")
            else:
                print("SSH connection failed with an error:", str(e))
                break
        except Exception as e:
            print("An error occurred:", str(e))
            attempts += 1
            if attempts <= 2:
                print("Retrying in 10 seconds...")
            else:
                break

        elapsed_time = time.time() - start_time
        if elapsed_time >= 60:
            print("Timeout: SSH service did not become active.")
            break

        time.sleep(10)

    return success

def configure_instance(instance_id):
    ensure_ec2()

    # Get the public IP address of the EC2 instance
    response = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the EC2 instance
    key_file_name = f"{key_name}.pem"
    ssh_key_filename = key_file_name

    if not wait_for_ssh(public_ip, username=ovpn_user_name, key_filename=ssh_key_filename):
        sys.exit(1)

    try:
        ssh_client.connect(public_ip, username=ovpn_user_name, key_filename=ssh_key_filename)

        # Execute the OpenVPN setup commands
        ssh_shell = ssh_client.invoke_shell()

        chunk = ""
        output = ""
        password = ""
        msg = ""
        while True:
            chunk = ssh_shell.recv(1024).decode("utf-8")
            if chunk:
                if chunk.endswith('\n'):
                    chunk = chunk[:-1] # Remove the trailing newline
                if debug:
                    print(chunk)
                output += chunk

            if not password:
                if (match := re.search(r"Please, remember this password (\w+)", output, re.DOTALL)):
                    password = match.group(1)


            if re.search(r"Please enter 'yes' to indicate your agreement \[no\]", output, re.DOTALL):
                ssh_shell.send("yes\n")
                output = ""
                time.sleep(1)
            
            if re.search(r"Should client traffic be routed by default through the VPN\?", output, re.DOTALL):
                ssh_shell.send("yes\n")
                otuput = ""
                time.sleep(1)

            
            if re.search(r"Type a password for the 'openvpn' account", output, re.DOTALL):
                ssh_shell.send("\n")
                output = ""
                time.sleep(1)

            if re.search(r"Please specify your Activation key \(or leave blank to specify later\)", output, re.DOTALL):
                ssh_shell.send("\n")
                output = ""
                time.sleep(1)

            if re.search(r"Press ENTER for default", output, re.DOTALL | re.IGNORECASE):
                ssh_shell.send("\n")
                output = ""
                time.sleep(1)

            if re.search(r"Press Enter for default", output, re.DOTALL):
                ssh_shell.send("\n")
                output = ""
                time.sleep(1)
            
            if re.search(r"Initial Configuration Complete!", output, re.DOTALL):
                msg = "OpenVPN configuration copleted."
                break

            if re.search(r"openvpnas@ip-(\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}):~\$", output, re.DOTALL):
                msg = "OpenVPN configuration previously completed."
                break
                

        print(f'''
--------------------------------------------------------------------------------

{msg}

Go to https://{public_ip}/admin and login:

  username: openvpn
  password: {password}


Go to User Management > User Profiles

Click on 'New Profile' to create a profile and download .opvn file. 

Install .opvn file in your favorite OpenVPN Client (e.g. Tunnelblick)

For killswitch, set 'On unexpected disconnect' = 'Disable network access'.

--------------------------------------------------------------------------------
''')

    finally:
        ssh_client.close()


def get_instance_id(stack_name):
    ensure_cfn()
    try:
        stack = cfn.describe_stacks(StackName=stack_name)['Stacks'][0]
        resources = stack['Outputs']
        for resource in resources:
            if resource['OutputKey'] == 'EC2InstanceId':
                return resource['OutputValue']
    except Exception as e:
        print(f"Error getting instance ID: {e}")
    return None


def ensure_instance(instance_id):
    ensure_ec2()
    try: 
        # Check if stack already exists
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        instance_status = instance['Reservations'][0]['Instances'][0]['State']['Name']
        if instance_status == 'stopped':
            start_instance(instance_id)
        elif instance_status not in ['pending', 'running']:
            print(f"Instance is in wrong status: {instance_status}")
            sys.exit(1)
    except Exception as e:
        print(f"Error getting instance state: {e}")
        sys.exit(1)


def wait_for_instance(instance_id, target_status = ['running']):
    if isinstance(target_status, str):
        target_status = [target_status] 
    ensure_ec2()
    while True:
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        instance_status = instance['Reservations'][0]['Instances'][0]['State']['Name']
        if instance_status in target_status:
            print(f"Instance {instance_id} is now {instance_status}.")
            break
        print(f"Waiting for Instance...  Instance status: {instance_status}")
        time.sleep(10)  # Wait for 10 seconds before checking again

def start_instance(instance_id):
    ensure_ec2()
    ec2.start_instances(InstanceIds=[instance_id])
    print("Starting instance...")

def stop_instance(instance_id):
    ensure_ec2()
    ec2.stop_instances(InstanceIds=[instance_id])
    print("Stopping instance...")


def print_info():
    ensure_ec2()
    instance_id = get_instance_id(stack_name)
    if instance_id:
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        instance_state = instance['Reservations'][0]['Instances'][0]['State']
        instance_status = instance_state['Name']
        print(f"Instance status: {instance_status}")
        try:
            public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
            key_file_name = f"{key_name}.pem"
            print(f"Public Ip Address: {public_ip}")
            print(f"ssh -i {key_file_name} {ovpn_user_name}@{public_ip}")
            print(f"https://{public_ip}")
        except Exception as e:
            pass


def delete_stack(stack_name):
    ensure_cfn()
    try:
        cfn.delete_stack(StackName=stack_name)
        print(f"CloudFormation stack '{stack_name}' deleted.")
    except cfn.exceptions.ClientError as e:
        if "does not exist" in str(e):
            print(f"CloudFormation stack '{stack_name}' not found.")
        else:
            print(f"Error deleting CloudFormation stack: {e}")

def delete_key_pair(key_name):
    ensure_ec2()
    # Delete EC2 key pair if it exists
    try:
        ec2.delete_key_pair(KeyName=key_name)
        print(f"EC2 key pair '{key_name}' deleted.")
    except ec2.exceptions.NoSuchKeyPair as e:
        print(f"EC2 key pair '{key_name}' not found.")


def command_up(args):
    # ensure_key_pair(key_name) # create_stack already callls ensure_key_pair
    ensure_stack(stack_name) 
    wait_for_stack(stack_name)
    instance_id = get_instance_id(stack_name)
    ensure_instance(instance_id)
    wait_for_instance(instance_id)
    configure_instance(instance_id)

def command_down(args):
    delete_stack(stack_name)
    delete_key_pair(key_name)
    
def command_key_up(args):
    ensure_key_pair(key_name)
    
def command_key_down(args):
    delete_key_pair(key_name)
    
def command_stack_up(args):
    create_stack(stack_name)
    wait_for_stack(stack_name)
    
def command_stack_down(args):
    delete_stack(stack_name)
    
def command_configure(args):
    instance_id = get_instance_id(stack_name)
    if instance_id:
        configure_instance(instance_id)
    
def command_start(args):
    instance_id = get_instance_id(stack_name)
    if instance_id:
        start_instance(instance_id)
        wait_for_instance(instance_id)
        print("Instance started.")
    
def command_stop(args):
    instance_id = get_instance_id(stack_name)
    if instance_id:
        stop_instance(instance_id)
        print("Instance stopped.")
    
def command_info(args):
    print_info()


class MyHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, indent_increment=2, max_help_position=42, width=None):
        super().__init__(prog, indent_increment, max_help_position, width=width)

    def _format_usage(self, usage, actions, groups, prefix):
        return f'usage: {self._prog} <options> command\n\n' 
    
    def _format_action_invocation(self, action):
        if action and hasattr(action, 'container') and action.container and hasattr(action.container, 'title') and action.container.title == 'commands':
            return 'DELETE'
        return super()._format_action_invocation(action)
    
    def _format_action(self, action):
        if action and hasattr(action, 'container') and action.container and hasattr(action.container, 'title') and action.container.title == 'commands':
            text = super()._format_action(action)
            return re.sub(r'\s*DELETE\n', '', text)
        return super()._format_action(action)

    # def format_help(self):
    #     help = super().format_help()
    #     if help:
    #         help = re.sub(r'optional arguments', 'Optional Arguments', help)
    #     return help

def main():
    # Define command-line arguments
    parser = argparse.ArgumentParser(
        description='AWS OpenVPN Tool',
        formatter_class=MyHelpFormatter
    )

    # Create a user-defined argument group
    parser.add_argument('-d', '--debug', action='store_true', help=argparse.SUPPRESS, default=None)
    parser.add_argument('-v', '--verbose', action='store_true', help="Turn on verbose", default=None)
    parser.add_argument('-k', '--key-file', help='Private Key file', default=None)
    
    parser.add_argument('--access-key-id', help='AWS access key ID', default=None)
    parser.add_argument('--secret-access-key', help='AWS secret access key', default=None)
    parser.add_argument('--profile', help='AWS profile name', default=None)
    parser.add_argument('--region', help='AWS region name', default=None)
    
    parser.add_argument('--instance-type', help="AWS Instance Type (default: %(default)s)", default=instance_type)
    parser.add_argument('--key-name', help="AWS Key Name (default: %(default)s)", default=key_name)
    parser.add_argument('--stack-name', help="AWS Stack Name (default: %(default)s)", default=stack_name)
    parser.add_argument('--ami-id', help="OpenVPN AMI ID (default: %(default)s)", default=ami_id)
    parser.add_argument('--opn-user-name', help="OpenVPN username (default: %(default)s)", default=ovpn_user_name)
    
    subparsers = parser.add_subparsers(title='commands', dest='command')
    parser_command = subparsers.add_parser('up', help='keyup, stackup, configure')
    parser_command.set_defaults(func=command_up)
    parser_command = subparsers.add_parser('down', help='keydown, stackdown')
    parser_command.set_defaults(func=command_down)
    parser_command = subparsers.add_parser('keyup', help='')
    parser_command.set_defaults(func=command_key_up)
    parser_command = subparsers.add_parser('keydown', help='')
    parser_command.set_defaults(func=command_key_down)
    parser_command = subparsers.add_parser('stackup', help='')
    parser_command.set_defaults(func=command_stack_up)
    parser_command = subparsers.add_parser('stackdown', help='')
    parser_command.set_defaults(func=command_stack_down)
    parser_command = subparsers.add_parser('start', help='')
    parser_command.set_defaults(func=command_start)
    parser_command = subparsers.add_parser('stop', help='')
    parser_command.set_defaults(func=command_stop)
    parser_command = subparsers.add_parser('configure', help='')
    parser_command.set_defaults(func=command_configure)
    parser_command = subparsers.add_parser('info', help='')
    parser_command.set_defaults(func=command_info)
    
    args = parser.parse_args()

    debug = args.debug

    # Load environment variables from the .env file
    load_dotenv()

    # Get AWS credentials and profile name from command-line arguments or environment variables
    access_key_id = args.access_key_id or os.environ.get('AWS_ACCESS_KEY_ID')
    secret_access_key = args.secret_access_key or os.environ.get('AWS_SECRET_ACCESS_KEY')
    profile_name = args.profile or os.environ.get('AWS_PROFILE')
    region_name = args.region or os.environ.get('AWS_REGION')

    if args.debug:
        print(f"access_key_id={access_key_id}")
        print(f"secret_access_key={secret_access_key}")
        print(f"profile_name={profile_name}")
        print(f"region_name={region_name}")

    # Create a boto3 session with specified credentials and profile
    session = create_boto3_session(access_key_id, secret_access_key, profile_name, region_name)


    if hasattr(args, 'func'):
        args.func(args)
    else:
        # parser.print_usage() 
        parser.print_help()
        sys.exit(0)
    




if __name__ == "__main__":
    main()

