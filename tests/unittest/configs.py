import datetime
import json

# Common Variables

DRY_RUN_YES = 'yes'
DRY_RUN_NO = 'no'
CURRENT_DATE = datetime.datetime.utcnow().date()
POLICY_COUNTER = 'DaysCount'


# AWS
AWS_DEFAULT_REGION = 'us-west-2'
DEFAULT_AMI_ID = 'ami-03cf127a'
INSTANCE_TYPE = 't2.micro'
ROLE_NAME = 'test-unittest-role-01'
ASSUME_ROLE_POLICY_DOCUMENT = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
})


# Azure
SUBSCRIPTION_ID = 'unitest-subscription'
RESOURCE_GROUP = 'unittest'
SUB_ID = f'/subscription/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}'
NETWORK_PROVIDER = f'providers/Microsoft.Network'
COMPUTE_PROVIDER = 'providers/Microsoft.Compute'
