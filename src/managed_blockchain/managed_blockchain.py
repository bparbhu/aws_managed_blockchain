import boto3

class ManagedBlockchain:
    def __init__(self):
        self.client = boto3.client("managedblockchain")

    def list_networks(self):
        """Lists all blockchain networks under AWS Managed Blockchain."""
        return self.client.list_networks()

    def get_transaction(self, transaction_hash, network="ETHEREUM_MAINNET"):
        """Fetch details of a specific transaction."""
        response = self.client.get_transaction(
            transactionHash=transaction_hash,
            network=network
        )
        return response["transaction"]
