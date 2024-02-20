from datetime import datetime, timedelta
import json

import boto3
from moto import mock_ec2, mock_s3, mock_iam

from cloud_governance.main.environment_variables import environment_variables
from cloud_governance.policy.aws.cleanup.unused_roles import UnusedRoles
from tests.unittest.configs import DRY_RUN_NO, AWS_DEFAULT_REGION, ROLE_NAME, ASSUME_ROLE_POLICY_DOCUMENT, \
    CURRENT_DATE, POLICY_COUNTER


@mock_iam
@mock_ec2
@mock_s3
def test_unused_roles_empty():
    """
    This method tests the unused roles delete
    :return:
    :rtype:
    """
    environment_variables.environment_variables_dict['DAYS_TO_TAKE_ACTION'] = 7
    environment_variables.environment_variables_dict['policy'] = 'unused_roles'
    environment_variables.environment_variables_dict['dry_run'] = DRY_RUN_NO
    environment_variables.environment_variables_dict['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION
    iam_client = boto3.client('iam')
    iam_client.create_role(AssumeRolePolicyDocument=ASSUME_ROLE_POLICY_DOCUMENT, RoleName=ROLE_NAME)
    unused_roles = UnusedRoles()
    response = unused_roles.run()
    assert len(iam_client.list_roles()['Roles']) == 1
    assert len(response) == 0



