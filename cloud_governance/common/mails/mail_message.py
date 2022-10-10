import json
import os


class MailMessage:

    RESTRICTION = 'Don\'t replay this email, in case of issue update us in slack channel #perf-dept-public-clouds.'

    def __init__(self):
        self.account = os.environ.get('account', '')
        self.policy = os.environ.get('policy', '')
        self.region = os.environ.get('AWS_DEFAULT_REGION', '')

    def ec2_stop(self, name: str, days: int, image_id: str, delete_instance_days: int, instance_name: str, resource_id: str, stopped_time: str, ec2_type: str):
        subject = f'cloud-governance alert: delete ec2-stop more than {days} days'
        content = 'This instance will be deleted after 30 days.\nPlease add Policy=Not_Delete to your tags for skipping this policy. If you already added ignore this email.'
        message = ''
        if image_id != '':
            content = f'You can find a image of the deleted image under AMI: {image_id}'
            message = f'This instance will be deleted due to it was stopped more than {delete_instance_days} days.'
        body = f"""
Greetings {name},

Instance: {instance_name}: {resource_id}( InstanceType:{ec2_type} ) in {self.region} on AWS account: {self.account} was stopped on {stopped_time}, it stopped more than {days} days.  
{message}
{content}

{self.RESTRICTION}

Best regards,
Cloud-governance Team""".strip()
        return subject, body

    def ec2_idle(self, name: str, days: int, notification_days: int, stop_days: int, instance_name: str, resource_id: str, ec2_type: str):
        if days == notification_days:
            subject = f'cloud-governance alert:  ec2-idle is {notification_days} days'
            cause = f'This instance will be stopped if it is idle {stop_days} days'
            content = 'If you want that cloud-governance will not stop it add Policy=Not_Delete tag to your instance. '
        else:
            subject = f'cloud-governance alert: Stopped ec2-idle more than {stop_days} days'
            cause = f'This instance will be stopped.'
            content = 'In future cloud-governance will not stop it add Policy=Not_Delete tag to your instance'
        body = f"""
Greetings {name},

Instance: {instance_name}: {resource_id} ( InstanceType:{ec2_type} ) in {self.region} on AWS account: {self.account} is idle more than {days} days.
{cause}
{content}
If you already added the Policy=Not_Delete tag ignore this mail.

{self.RESTRICTION}

Best Regards,
Cloud-governance Team""".strip()
        return subject, body

    def iam_user_add_tags(self, name: str, user: str, spreadsheet_id: str):
        subject = f'cloud-governance alert: Missing tags in AWS IAM User'
        body = f"""
Hi {name},

{os.environ.get('account')} IAM User: {user} has missing tags 
Please add the tags in the spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}.
If you already filled the tags, please ignore the mail.

{self.RESTRICTION}

Best Regards
Cloud-governance Team""".strip()
        return subject, body

    def aws_user_over_usage_cost(self, user: str, usage_cost: int, name: str, user_usage: int):
        """
        This method send subject, body to over usage cost
        @return:
        """
        subject = f'cloud-governance alert: last week cost over usage {usage_cost}$ per user'
        body = f"""
Hi {name},
Your AWS user:{user} in account:{os.environ.get('account')} cost was {user_usage}$ in the last week. 
Please verify that you are using all the resources.
Please verify that you are using all the resources in attached {user}_resource.json file.

{self.RESTRICTION}

Best Regards,
Cloud-governance Team""".strip()
        return subject, body

    def resource_message(self, name: str, days: int, notification_days: int, delete_days: int, resource_name: str, resource_id: str, resource_type: str, resources: list = []):
        """
        This method prepare mail message based on resource_type and return subject, body
        @param resources:
        @param name:
        @param days:
        @param notification_days:
        @param delete_days:
        @param resource_name:
        @param resource_id:
        @param resource_type:
        @return:
        """
        resource_type = resource_type.capitalize()
        reason = self.policy.split('_')[-1]
        if 'empty' in self.policy:
            reason = 'empty'
        if 'zombie' in self.policy:
            reason = 'Unused'
        if days == notification_days:
            subject = f'cloud-governance alert: {self.policy} is {reason} since {notification_days} days'
            cause = f'This {resource_type} will be deleted if it is {reason} {delete_days} days'
            content = f'If you want that cloud-governance will not delete it add Policy=Not_Delete/skip tag to your {resource_type}s.'
        else:
            subject = f'cloud-governance alert: Deleted {self.policy} is {reason} more than {delete_days} days'
            cause = f'This {resource_type} will be deleted due to it was {reason} more than {delete_days} days.'
            content = f'In future cloud-governance will not delete your {resource_type} add Policy=Not_Delete/skip tag to your {resource_type}s'
        extra_data = ''
        if resources:
            extra_data = f'Cluster Undeleted Resources: {sorted(resources)}'
        body = f"""
Greetings {name},

{resource_type}: {resource_name}: {resource_id} in {self.region} on AWS account: {self.account} is {reason} more than {days} days.
{cause}
{content}
If you already added the Policy=Not_Delete/skip tag ignore this mail.

{extra_data}

{self.RESTRICTION}

Best Regards,
Cloud-governance Team""".strip()
        return subject, body
