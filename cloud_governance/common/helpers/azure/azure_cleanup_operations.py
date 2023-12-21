
from cloud_governance.common.clouds.azure.compute.compute_operations import ComputeOperations
from cloud_governance.common.clouds.azure.compute.resource_group_operations import ResourceGroupOperations
from cloud_governance.common.helpers.cleanup_operations import AbstractCleanUpOperations
from cloud_governance.common.logger.init_logger import logger
from cloud_governance.common.utils.utils import Utils


class AzureCleaUpOperations(AbstractCleanUpOperations):

    def __init__(self):
        super().__init__()
        self._cloud_name = 'Azure'
        self.compute_operations = ComputeOperations()
        self.resource_group_operations = ResourceGroupOperations()

    def get_tag_name_from_tags(self, tags: dict, tag_name: str):
        """
        This method returns the tag value by the tag_name
        :param tags:
        :type tags:
        :param tag_name:
        :type tag_name:
        :return:
        :rtype:
        """
        if tags:
            for key, value in tags.items():
                if Utils.equal_ignore_case(key, tag_name):
                    return value
        return ''

    def _delete_resource(self, resource_id: str):
        """
        This method deletes the
        :param resource_id:
        :type resource_id:
        :return:
        :rtype:
        """
        action = "deleted"
        try:
            if self._policy == 'vm_run':
                action = "Stopped"
                self.compute_operations.stop_vm(resource_id=resource_id)
            logger.info(f'{self._policy} {action}: {resource_id}')
        except Exception as err:
            logger.info(f'Exception raised: {err}: {resource_id}')

    def update_resource_day_count_tag(self, resource_id: str, cleanup_days: int, tags: dict):
        tags = self._update_tag_value(tags=tags, tag_name='DaysCount', tag_value=str(cleanup_days))
        try:
            if self._policy == 'vm_run':
                self.resource_group_operations.creates_or_updates_tags(resource_id=resource_id, tags=tags)
        except Exception as err:
            logger.info(f'Exception raised: {err}: {resource_id}')

    def _update_tag_value(self, tags: dict, tag_name: str, tag_value: str):
        """
        This method returns the updated tag_list by adding the tag_name and tag_value to the tags
        @param tags:
        @param tag_name:
        @param tag_value:
        @return:
        """
        if self._dry_run == "yes":
            tag_value = 0
        tag_value = f'{self.CURRENT_DATE}@{tag_value}'
        found = False
        updated_tags = {}
        if tags:
            for key, value in tags.items():
                if Utils.equal_ignore_case(key, tag_name):
                    if value.split("@")[0] != self.CURRENT_DATE:
                        updated_tags[key] = tag_value
                    else:
                        if int(tag_value.split("@")[-1]) == 0 or int(tag_value.split("@")[-1]) == 1:
                            updated_tags[key] = tag_value
                    found = True
        tags.update(updated_tags)
        if not found:
            return {tag_name: tag_value}
        return tags
