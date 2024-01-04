# awsovpn

Manage an OpenVPN instance in your private EC2 cloud using this script. 


## Usage

1. Create an OpenVPN EC2 instance and configure it for VPN access.

    ```bash
    awsovpn up
    ```

    Then following instructions to configure a Profile and install in your local OpenVPN client.

2. Terminate the OpenVPN EC2 instance and remove all EC2 resources mangaed by this script:

    ```bash
    awsovpn down
    ```



## Install

```bash
python -m pip install awsovpn
```

## Configure

Configure using any of combination of the following methods:

1. awscli configuration

    If you have [awscli](https://aws.amazon.com/cli/) installed and configured, then awsovpn can utilize this same configuration. Just use `--profile PROFILE` to specify an AWS configuration profile. 

    ```bash
    awsovpn --profile myprofile up
    ``````

2. environment variables

    Create a `.env` file or set the following environment variables: 

    ```text
    AWS_REGION=
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_PROFILE=
    ```

3. use arguments

    You can also pass credential configuration as arguments:

    e.g.

    ```bash
    awsovpn --region REGION --access-key-id ACCESS_KEY_ID --secret-access-key SECRET_ACCESS_KEY
    ```
