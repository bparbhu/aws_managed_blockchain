class ManagedBlockchainPaginator:
    def __init__(self):
        self.client = boto3.client("managedblockchain-query")

    def paginate_transactions(self, address, network="ETHEREUM_MAINNET"):
        """Uses paginator to list all transactions."""
        paginator = self.client.get_paginator("list_transactions")
        response_iterator = paginator.paginate(
            address=address,
            network=network
        )
        transactions = []
        for page in response_iterator:
            transactions.extend(page["transactions"])
        return transactions
