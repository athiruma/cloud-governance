import json
import os


access_id = os.environ['access_id']
secret_key = os.environ['secret_key']
bucket = os.environ['bucket']
account_name = os.environ['account_name']
LDAP_HOST_NAME = os.environ['LDAP_HOST_NAME']

LOGS = os.environ.get('LOGS', 'logs')


os.system(f"""echo "Running the tag_resources" """)
regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'eu-central-1', 'ap-south-1', 'eu-north-1', 'ap-northeast-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-west-3', 'sa-east-1']

mandatory_tags = {"Budget": account_name}
for region in regions:
    os.system(f"""podman run --rm --net="host" --name cloud-governance-poc-haim-hourly -e account="{account_name}" -e EMAIL_ALERT="False" -e policy="tag_resources" -e AWS_ACCESS_KEY_ID="{access_id}" -e AWS_SECRET_ACCESS_KEY="{secret_key}" -e AWS_DEFAULT_REGION="{region}" -e tag_operation="update" -e mandatory_tags="{mandatory_tags}" -e log_level="INFO" -v "/etc/localtime":"/etc/localtime" docker.io/thirumaleshaaraveti/cloud-governance:latest""")
