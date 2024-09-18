import os

ES_HOST = os.environ['ES_HOST']
ES_PORT = os.environ['ES_PORT']
TO_MAIL = os.environ['TO_MAIL']
CC_MAIL = os.environ['CC_MAIL']
QUAY_CLOUD_GOVERNANCE_REPOSITORY = os.environ.get('QUAY_CLOUD_GOVERNANCE_REPOSITORY',
                                                  'quay.io/cloud-governance/cloud-governance:latest')

LOGS = os.environ.get('LOGS', 'logs')

# RUN AWS Monthly Policies
print("Run AWS Monthly Policies")
os.system(
    f"""podman run --rm --name cloud-governance --net="host" -e policy="monthly_report" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e to_mail="{TO_MAIL}" -e cc_mail="{CC_MAIL}" -e log_level="INFO" {QUAY_CLOUD_GOVERNANCE_REPOSITORY}""")
