from cloud_governance.common.helpers.azure.azure_cleanup_operations import AzureCleaUpOperations


class VmRun(AzureCleaUpOperations):

    RESOURCE_ACTION = "Stopped"

    def __init__(self):
        super().__init__()

    def __get_instance_status(self, resource_id: str, vm_name: str):
        """
        This method returns the VM status of the Virtual Machine
        :param resource_id:
        :type resource_id:
        :param vm_name:
        :type vm_name:
        :return:
        :rtype:
        """
        instance_statuses = self.compute_operations.get_instance_statuses(resource_id=resource_id, vm_name=vm_name)
        statuses = instance_statuses.get('statuses', {})
        if len(statuses) >= 2:
            status = statuses[1].get('display_status', '').lower()
        elif len(statuses) == 1:
            status = statuses[0].get('display_status', '').lower()
        else:
            status = 'Unknown Status'
        return status

    def __vm_run(self):
        """
        This method returns the running vms in the AAzure cloud and stops based on the action
        :return:
        :rtype:
        """
        vms_list = self.compute_operations.get_all_instances()
        running_vms = []
        for vm in vms_list:
            status = self.__get_instance_status(resource_id=vm.id, vm_name=vm.name)
            tags = vm.tags if vm.tags else {}
            if 'running' in status:
                running_days = self.calculate_days(vm.time_created)
                cleanup_days = self.get_clean_up_days_count(tags=tags)
                cleanup_result = self.verify_and_delete_resource(resource_id=vm.id, tags=tags,
                                                                 clean_up_days=cleanup_days)
                resource_data = {
                    'ResourceId': vm.name,
                    'VmId': vm.vm_id,
                    'User': self.get_tag_name_from_tags(tags=tags, tag_name='User'),
                    'SkipPolicy': self.get_skip_policy_value(tags=tags),
                    'LaunchTime': vm.time_created,
                    'InstanceType': vm.hardware_profile.vm_size,
                    'InstanceState': status if cleanup_result else 'Vm Stopped',
                    'RunningDays': running_days,
                    'CleanUpDays': cleanup_days,
                    'DryRun': self._dry_run,
                    'Name': vm.name,
                    'RegionName': vm.location,
                    f'Resource{self.RESOURCE_ACTION}': str(cleanup_result),
                    'PublicCloud': self._cloud_name
                }
                if self._force_delete and self._dry_run == 'no':
                    resource_data.update({'ForceDeleted': str(self._force_delete)})
                running_vms.append(resource_data)
            else:
                cleanup_days = 0
            self.update_resource_day_count_tag(resource_id=vm.id, cleanup_days=cleanup_days, tags=tags)
        return running_vms

    def run(self):
        """
        This method starts the VMRun operations
        :return:
        :rtype:
        """
        return self.__vm_run()
