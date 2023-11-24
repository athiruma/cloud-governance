

import importlib
import inspect

from cloud_governance.common.logger.init_logger import logger
from cloud_governance.main.environment_variables import environment_variables


class AWSPolicyRunner:
    """
    This method run the Common policies
    """

    def __init__(self):
        self.__environment_variables_dict = environment_variables.environment_variables_dict
        self._policy = self.__environment_variables_dict.get('policy')
        self._cloud_name = self.__environment_variables_dict.get('PUBLIC_CLOUD_NAME')
        self._account = self.__environment_variables_dict.get('account')
        self._dry_run = self.__environment_variables_dict.get('dry_run')

    def run(self):
        """
        Run the Common policies
        @return:
        """
        aws_policies = importlib.import_module(f'cloud_governance.policy.aws.{self._policy}')
        logger.info(f'CLOUD_NAME: {self._cloud_name}, Account: {self._account}, Policy: {self._policy}, dry_run: {self._dry_run}')
        for cls in inspect.getmembers(aws_policies, inspect.isclass):
            if self._policy.replace('_', '') == cls[0].lower():
                response = cls[1]().run()
                if isinstance(response, list) and len(response) > 0:
                    logger.info(f'key: {cls[0]}, count: {len(response)}, {response}')
