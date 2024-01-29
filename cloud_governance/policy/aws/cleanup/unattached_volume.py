

from cloud_governance.policy.helpers.aws.aws_policy_operations import AWSPolicyOperations
from cloud_governance.common.utils.utils import Utils


class UnattachedVolume(AWSPolicyOperations):

    RESOURCE_ACTION = "Delete"

    def __init__(self):
        super().__init__()

    def run_policy_operations(self):
        """
        This method returns the list of unattached volumes
        :return:
        :rtype:
        """
        unattached_volumes = []
        available_volumes = self._get_all_volumes()
        for volume in available_volumes:
            tags = volume.get('Tags', [])
            resource_id = volume.get('VolumeId')
            cleanup_result = False
            if Utils.equal_ignore_case(volume.get('State'), 'available'):
                cleanup_days = self.get_clean_up_days_count(tags=tags)
                cleanup_result = self.verify_and_delete_resource(resource_id=resource_id, tags=tags,
                                                                 clean_up_days=cleanup_days)
                resource_data = self._get_es_schema(resource_id=resource_id,
                                                    user=self.get_tag_name_from_tags(tags=tags, tag_name='User'),
                                                    skip_policy=self.get_skip_policy_value(tags=tags),
                                                    cleanup_days=cleanup_days, dry_run=self._dry_run,
                                                    name=self.get_tag_name_from_tags(tags=tags, tag_name='Name'),
                                                    region=self._region,
                                                    cleanup_result=str(cleanup_result),
                                                    resource_action=self.RESOURCE_ACTION,
                                                    cloud_name=self._cloud_name,
                                                    resource_type=volume.get('VolumeType', ''),
                                                    resource_state=volume.get('State') if not cleanup_result else "Deleted",
                                                    volume_size=f"{volume.get('Size')} GB"
                                                    )
                unattached_volumes.append(resource_data)
            else:
                cleanup_days = 0
            if not cleanup_result:
                self.update_resource_day_count_tag(resource_id=resource_id, cleanup_days=cleanup_days, tags=tags)

        return unattached_volumes

