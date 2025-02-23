import boto3
import botocore

class ManagedBlockchainPaginator:
    def __init__(self):
        """Initialize the Managed Blockchain client."""
        self.client = boto3.client('managedblockchain')

    def get_paginator(self, operation_name: str):
        """
        Creates a paginator for an operation.

        :param operation_name: The operation name (e.g., "list_networks", "list_members").
        :return: A paginator object or None if the operation is not pageable.
        """
        try:
            if not self.client.can_paginate(operation_name):
                print(f"Operation '{operation_name}' is not pageable.")
                return None

            paginator = self.client.get_paginator(operation_name)
            return paginator
        except botocore.exceptions.OperationNotPageableError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

        return None

    def paginate_operation(self, operation_name: str, **kwargs):
        """
        Paginates through a Managed Blockchain operation.

        :param operation_name: The operation to paginate (e.g., "list_members", "list_networks").
        :param kwargs: Additional parameters required by the operation.
        :return: A list of results from all pages.
        """
        paginator = self.get_paginator(operation_name)
        if paginator is None:
            return []

        results = []
        try:
            for page in paginator.paginate(**kwargs):
                results.extend(page.get(operation_name.capitalize(), []))
        except Exception as e:
            print(f"Error while paginating '{operation_name}': {e}")

        return results
