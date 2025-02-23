import boto3

class ManagedBlockchainQueryTransactionEvents:
    def __init__(self):
        self.client = boto3.client('managedblockchain-query')

    def list_transaction_events(self, transaction_hash: str, network: str):
        """Lists all transaction events for a given transaction."""
        return self.client.list_transaction_events(transactionHash=transaction_hash, network=network)
