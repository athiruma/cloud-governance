

import json

from cloud_governance.cloud_resource_orchestration.common.abstract_monitor_tickets import AbstractMonitorTickets
from cloud_governance.common import logger_time_stamp


class AzureMonitorTickets(AbstractMonitorTickets):
    """This method monitors the Jira Tickets"""

    NEW = 'New'
    REFINEMENT = 'Refinement'
    CLOSED = 'Closed'
    IN_PROGRESS = 'In Progress'
    CLOSE_JIRA_TICKET = 0
    FIRST_CRO_ALERT: int = 5
    SECOND_CRO_ALERT: int = 3
    DEFAULT_ROUND_DIGITS: int = 3

    def __init__(self, region_name: str = ''):
        super().__init__()

    # Todo All the below methods implement in future releases
    def update_budget_tag_to_resources(self, region_name: str, ticket_id: str, updated_budget: int):
        pass

    def update_duration_tag_to_resources(self, region_name: str, ticket_id: str, updated_duration: int):
        pass

    def update_cluster_cost(self):
        pass

    def extend_tickets_budget(self, ticket_id: str, region_name: str, current_budget: int = 0):
        return super().extend_tickets_budget(ticket_id, region_name, current_budget)

    def extend_ticket_duration(self, ticket_id: str, region_name: str, current_duration: int = 0):
        return super().extend_ticket_duration(ticket_id, region_name, current_duration)

    @logger_time_stamp
    def run(self):
        """
        This method run all methods of jira tickets monitoring
        :return:
        # """
        self.monitor_tickets()




