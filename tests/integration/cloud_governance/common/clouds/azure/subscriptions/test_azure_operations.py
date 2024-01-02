from cloud_governance.common import AzureOperations


def test_get_subscription_id():
    """
    This method test we get the subscription id from the azure
    @return:
    """
    azure_operations = AzureOperations()
    subscription_id = azure_operations.subscription_id
    assert subscription_id
