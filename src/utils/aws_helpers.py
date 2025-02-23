import boto3

class ManagedBlockchainUtils:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def can_paginate(self, operation_name: str):
        """Checks if an operation supports pagination."""
        return self.client.can_paginate(operation_name)

    def get_paginator(self, operation_name: str):
        """Returns a paginator for an operation."""
        return self.client.get_paginator(operation_name)

    def get_waiter(self, waiter_name: str):
        """Returns a waiter object for a given operation."""
        return self.client.get_waiter(waiter_name)

    def close(self):
        """Closes the client connection."""
        self.client.close()
