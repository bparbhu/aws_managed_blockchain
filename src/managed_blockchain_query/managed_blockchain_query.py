class ManagedBlockchainQuery:
    def __init__(self):
        self.client = boto3.client("managedblockchain-query")

    def list_token_balances(self, owner_address, network="ETHEREUM_MAINNET"):
        """Lists all token balances owned by an address."""
        response = self.client.list_token_balances(
            ownerFilter={"address": owner_address},
            tokenFilter={"network": network}
        )
        return response["tokenBalances"]

    def list_asset_contracts(self, deployer_address, network="ETHEREUM_MAINNET"):
        """Lists all contracts deployed by a specific address."""
        response = self.client.list_asset_contracts(
            contractFilter={"network": network, "deployerAddress": deployer_address}
        )
        return response["contracts"]
