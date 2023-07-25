import json
import os


HAIM_CREDS = os.environ['HAIM_CREDS']
AWS_SECRET_ACCESS_KEY_APPENG = os.environ['AWS_SECRET_ACCESS_KEY_APPENG']
LDAP_HOST_NAME = os.environ['LDAP_HOST_NAME']
LOGS = os.environ.get('LOGS', 'logs')
ES_HOST = os.environ['ES_HOST']
ES_PORT = os.environ['ES_PORT']
BUCKET_APPENG = os.environ['BUCKET_APPENG']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
SPREADSHEET_ID = os.environ['AWS_IAM_USER_SPREADSHEET_ID']


def get_policies(type: str = None):
    """
    This method return a list of policies name without extension, that can filter by type
    @return: list of policies name
    """
    policies = []
    policies_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), 'cloud_governance', 'policy', 'aws')
    for (dirpath, dirnames, filenames) in os.walk(policies_path):
        for filename in filenames:
            if not filename.startswith('__') and (filename.endswith('.yml') or filename.endswith('.py')):
                if not type:
                    policies.append(os.path.splitext(filename)[0])
                elif type and type in filename:
                    policies.append(os.path.splitext(filename)[0])
    return policies


regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'eu-central-1', 'ap-south-1', 'eu-north-1', 'ap-northeast-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-west-3', 'sa-east-1']
policies = get_policies()
not_action_policies = ['cost_explorer', 'cost_over_usage', 'monthly_report', 'cost_billing_reports', 'cost_explorer_payer_billings']
run_policies = list(set(policies) - set(not_action_policies))
run_policies.sort()

with open(HAIM_CREDS) as file:
    aws_accounts = json.load(file)

run_policies.remove('ebs_in_use')
run_policies.remove('ec2_run')
es_doc_type = '_doc'

cost_tags = ['PurchaseType', 'ChargeType', 'User', 'Budget', 'Project', 'Manager', 'Owner', 'LaunchTime', 'Environment', 'User:Spot']
cost_metric = 'UnblendedCost'  # UnblendedCost/BlendedCost
granularity = 'DAILY'  # DAILY/MONTHLY/HOURLY
cost_explorer_index = 'cloud-governance-haim-cost-explorer-global-index'
os.system(f"""echo "Running the CloudGovernance CostExplorer Policies" """)
for account_name, account_values in aws_accounts.items():
    access_id = account_values.get("AWS_ACCESS_KEY_ID")
    secret_key = account_values.get('AWS_SECRET_ACCESS_KEY')
    bucket = account_values.get('BUCKET')
    os.system(f"""podman run --rm --name cloud-governance-daily --net="host" -e account="{account_name}" -e AWS_ACCESS_KEY_ID="{access_id}" -e AWS_SECRET_ACCESS_KEY="{secret_key}"  -e AWS_DEFAULT_REGION="us-east-1"  -e policy="cost_explorer"  -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e es_index="{cost_explorer_index}" -it -e cost_explorer_tags="{cost_tags}" -e granularity="{granularity}" -e cost_metric="{cost_metric}" -e policy_output="s3://{bucket}/{LOGS}/us-east-1" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")

# run_policies = ['ebs_unattached', 'ip_unattached', 's3_inactive']
os.system(f"""echo Running the cloud_governance policies: {run_policies}""")
os.system(f"""echo "Running the CloudGovernance policies" """)
for account_name, account_values in aws_accounts.items():
    access_id = account_values.get("AWS_ACCESS_KEY_ID")
    secret_key = account_values.get('AWS_SECRET_ACCESS_KEY')
    bucket = account_values.get('BUCKET')
    for region in regions:
        for policy in run_policies:
            if policy in ('empty_roles', 's3_inactive') and region == 'us-east-1':
                os.system(f"""podman run --rm --name cloud-governance-daily --net="host" -e account="{account_name}" -e AWS_ACCESS_KEY_ID="{access_id}" -e AWS_SECRET_ACCESS_KEY="{secret_key}" -e MANAGER_EMAIL_ALERT="False" -e EMAIL_ALERT="False"  -e policy="{policy}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="yes" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e log_level="INFO" -e policy_output="s3://{bucket}/{LOGS}/{region}" quay.io/ebattat/cloud-governance:latest""")
            elif policy not in ('empty_roles', 's3_inactive'):
                os.system(f"""podman run --rm --name cloud-governance-daily --net="host" -e account="{account_name}" -e AWS_ACCESS_KEY_ID="{access_id}" -e AWS_SECRET_ACCESS_KEY="{secret_key}" -e MANAGER_EMAIL_ALERT="False" -e EMAIL_ALERT="False" -e policy="{policy}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="yes" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e log_level="INFO" -e policy_output="s3://{bucket}/{LOGS}/{region}" quay.io/ebattat/cloud-governance:latest""")
            if policy in ['zombie_cluster_resource'] and region == 'us-east-1':
                os.system(f"""podman run --rm --name cloud-governance-daily -e upload_data_es="upload_data_es" -e account="{account_name}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e es_doc_type="{es_doc_type}" -e bucket="{bucket}" -e policy="{policy}" -e AWS_DEFAULT_REGION="{region}" -e AWS_ACCESS_KEY_ID="{access_id}" -e AWS_SECRET_ACCESS_KEY="{secret_key}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")

os.system(f"""echo "Running the tag_iam_user" """)
for account_name, account_values in aws_accounts.items():
    access_id = account_values.get("AWS_ACCESS_KEY_ID")
    secret_key = account_values.get('AWS_SECRET_ACCESS_KEY')
    bucket = account_values.get('BUCKET')
    os.system(f"""podman run --rm --name cloud-governance-hourly --net="host" \
    -e account="{account_name}" \
    -e AWS_ACCESS_KEY_ID="{access_id}" -e AWS_SECRET_ACCESS_KEY="{secret_key}" \
    -e EMAIL_ALERT="False" \
    -e policy="tag_iam_user" \
    -e user_tag_operation="update"  \
    -e SPREADSHEET_ID="{SPREADSHEET_ID}" \
    -e GOOGLE_APPLICATION_CREDENTIALS="{GOOGLE_APPLICATION_CREDENTIALS}" \
    -v "{GOOGLE_APPLICATION_CREDENTIALS}":"{GOOGLE_APPLICATION_CREDENTIALS}" \
    -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
