import boto3

class ManagedBlockchainQueryContracts:
    def __init__(self):
        self.client = boto3.client('managedblockchain-query')

    def list_contracts(self, deployer_address: str, network: str, token_standard: str):
        """Lists all contracts deployed by an address."""
        return self.client.list_asset_contracts(
            contractFilter={"network": network, "tokenStandard": token_standard, "deployerAddress": deployer_address}
        )
