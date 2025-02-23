import boto3

class ManagedBlockchainQueryTokenBalances:
    def __init__(self):
        self.client = boto3.client('managedblockchain-query')

    def list_token_balances(self, address: str, network: str):
        """Lists all token balances for an address."""
        return self.client.list_token_balances(ownerFilter={"address": address}, tokenFilter={"network": network})
