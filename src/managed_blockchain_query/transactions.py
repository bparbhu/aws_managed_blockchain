import boto3

class ManagedBlockchainQueryTransactions:
    def __init__(self):
        self.client = boto3.client('managedblockchain-query')

    def get_transaction(self, transaction_hash: str, network: str):
        """Retrieves details of a specific transaction."""
        return self.client.get_transaction(transactionHash=transaction_hash, network=network)

    def list_transactions(self, address: str, network: str):
        """Lists all transactions for a given address."""
        return self.client.list_transactions(address=address, network=network)
