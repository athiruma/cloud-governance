from abc import ABC, abstractmethod

from cloud_governance.common import ComputeOperations
from cloud_governance.common import ResourceGroupOperations


class AbstractResource(ABC):

    def __init__(self):
        self._resource_group_operations = ResourceGroupOperations()
        self._compute_client = ComputeOperations()

    @abstractmethod
    def run(self):
        pass
