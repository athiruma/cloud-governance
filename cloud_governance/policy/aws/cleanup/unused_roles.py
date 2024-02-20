
from cloud_governance.policy.helpers.aws.aws_policy_operations import AWSPolicyOperations
from cloud_governance.common.utils.utils import Utils

# @Todo Add the unittest cases


class UnusedRoles(AWSPolicyOperations):
    """
    This policy will delete the roles which are not being used.
    by default will delete roles > 7 days. you can customize by DAYS_TO_TAKE_ACTION env var
    """

    RESOURCE_ACTION = "Delete"

    def __init__(self):
        super().__init__()

    def run_policy_operations(self):
        """
        This method returns the list of unattached volumes
        :return:
        :rtype:
        """
        unused_roles = []
        roles = self._iam_operations.list_roles()
        active_cluster_ids = self._get_active_cluster_ids()
        for role in roles:
            role_name = role.get('RoleName')
            if not role_name.startswith('AWS'):
                cleanup_result = False
                role_data = self._iam_operations.get_role(role_name=role_name)
                tags = role_data.get('Tags', [])
                cluster_tag = self._get_cluster_tag(tags=tags)
                role_last_used = role_data.get('RoleLastUsed', {}).get('LastUsedDate')
                if not role_last_used:
                    role_last_used = role_data.get('CreateDate')
                role_age = self.calculate_days(role_last_used)
                if cluster_tag not in active_cluster_ids and role_age > self._days_to_take_action:
                    cleanup_days = self.get_clean_up_days_count(tags=tags)
                    cleanup_result = self.verify_and_delete_resource(resource_id=role_name, tags=tags,
                                                                     clean_up_days=cleanup_days)
                    resource_data = self._get_es_schema(resource_id=role_name,
                                                        user=self.get_tag_name_from_tags(tags=tags, tag_name='User'),
                                                        skip_policy=self.get_skip_policy_value(tags=tags),
                                                        cleanup_days=cleanup_days, dry_run=self._dry_run,
                                                        name=role_name,
                                                        region=self._region,
                                                        cleanup_result=str(cleanup_result),
                                                        resource_action=self.RESOURCE_ACTION,
                                                        cloud_name=self._cloud_name,
                                                        resource_type='IAM Role',
                                                        resource_state='UnUsed' if not cleanup_result else "Deleted"
                                                        )
                    unused_roles.append(resource_data)
                else:
                    cleanup_days = 0
                if not cleanup_result:
                    self.update_resource_day_count_tag(resource_id=role_name, cleanup_days=cleanup_days, tags=tags)

        return unused_roles
