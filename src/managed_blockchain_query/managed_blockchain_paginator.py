import boto3
import botocore
from datetime import datetime
from typing import Optional, Dict, Any, List


class ManagedBlockchainPaginator:
    def __init__(self):
        self.client = boto3.client("managedblockchain-query")

    def paginate_list_asset_contracts(
        self,
        network: str,
        token_standard: str,
        deployer_address: str,
        max_items: Optional[int] = None,
        page_size: Optional[int] = None,
        starting_token: Optional[str] = None
    ) -> List[Dict]:
        """
        Paginates through asset contracts.

        :param network: The blockchain network (ETHEREUM_MAINNET, ETHEREUM_SEPOLIA_TESTNET, BITCOIN_MAINNET, BITCOIN_TESTNET).
        :param token_standard: The token standard (ERC20, ERC721, ERC1155).
        :param deployer_address: The address that deployed the contract.
        :param max_items: (Optional) The total number of items to return.
        :param page_size: (Optional) The size of each page.
        :param starting_token: (Optional) Token to specify where to start paginating.

        :return: List of asset contracts.
        """
        try:
            paginator = self.client.get_paginator("list_asset_contracts")
            response_iterator = paginator.paginate(
                contractFilter={
                    "network": network,
                    "tokenStandard": token_standard,
                    "deployerAddress": deployer_address,
                },
                PaginationConfig={
                    "MaxItems": max_items,
                    "PageSize": page_size,
                    "StartingToken": starting_token,
                }
            )

            results = []
            for page in response_iterator:
                results.extend(page.get("contracts", []))

            return results

        except botocore.exceptions.ClientError as e:
            print(f"Client error occurred: {e}")
            return {"error": str(e)}
        except botocore.exceptions.BotoCoreError as e:
            print(f"BotoCore error occurred: {e}")
            return {"error": str(e)}

    def paginate_list_filtered_transaction_events(
        self,
        network: str,
        transaction_event_to_address: List[str],
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        vout_spent: Optional[bool] = None,
        confirmation_status: Optional[List[str]] = None,
        sort_by: str = "blockchainInstant",
        sort_order: str = "ASCENDING",
        max_items: Optional[int] = None,
        page_size: Optional[int] = None,
        starting_token: Optional[str] = None
    ) -> List[Dict]:
        """
        Paginates through filtered transaction events for an address on the blockchain.

        :param network: The blockchain network (BITCOIN_MAINNET | BITCOIN_TESTNET).
        :param transaction_event_to_address: List of recipient addresses for filtering transactions.
        :param from_time: Start time for filtering transactions.
        :param to_time: End time for filtering transactions.
        :param vout_spent: Filter based on whether the transaction output is spent.
        :param confirmation_status: Filter transactions based on confirmation status (FINAL or NONFINAL).
        :param sort_by: Sorting criteria (default: "blockchainInstant").
        :param sort_order: Sorting order (ASCENDING or DESCENDING).
        :param max_items: (Optional) The total number of items to return.
        :param page_size: (Optional) The size of each page.
        :param starting_token: (Optional) Token to specify where to start paginating.

        :return: List of filtered transaction events.
        """
        try:
            paginator = self.client.get_paginator("list_filtered_transaction_events")

            request_params = {
                "network": network,
                "addressIdentifierFilter": {"transactionEventToAddress": transaction_event_to_address},
                "sort": {"sortBy": sort_by, "sortOrder": sort_order}
            }

            if from_time or to_time:
                request_params["timeFilter"] = {}
                if from_time:
                    request_params["timeFilter"]["from"] = {"time": from_time}
                if to_time:
                    request_params["timeFilter"]["to"] = {"time": to_time}

            if vout_spent is not None:
                request_params["voutFilter"] = {"voutSpent": vout_spent}

            if confirmation_status:
                request_params["confirmationStatusFilter"] = {"include": confirmation_status}

            pagination_config = {
                "MaxItems": max_items,
                "PageSize": page_size,
                "StartingToken": starting_token,
            }
            response_iterator = paginator.paginate(**request_params, PaginationConfig=pagination_config)

            results = []
            for page in response_iterator:
                results.extend(page.get("events", []))

            return results

        except botocore.exceptions.ClientError as e:
            print(f"Client error occurred: {e}")
            return {"error": str(e)}
        except botocore.exceptions.BotoCoreError as e:
            print(f"BotoCore error occurred: {e}")
            return {"error": str(e)}

    def paginate_list_token_balances(
        self,
        network: str,
        contract_address: Optional[str] = None,
        token_id: Optional[str] = None,
        owner_address: Optional[str] = None,
        max_items: Optional[int] = None,
        page_size: Optional[int] = None,
        starting_token: Optional[str] = None
    ) -> List[Dict]:
        """
        Paginates through token balances for an address, contract, or specific token.

        :param network: The blockchain network (ETHEREUM_MAINNET, ETHEREUM_SEPOLIA_TESTNET, BITCOIN_MAINNET, BITCOIN_TESTNET).
        :param contract_address: (Optional) The contract address for filtering balances.
        :param token_id: (Optional) The unique identifier for a specific token.
        :param owner_address: (Optional) The wallet or contract address to check balances for.
        :param max_items: (Optional) The total number of items to return.
        :param page_size: (Optional) The size of each page.
        :param starting_token: (Optional) Token to specify where to start paginating.

        :return: List of token balance details.
        """
        try:
            paginator = self.client.get_paginator("list_token_balances")

            request_params = {
                "tokenFilter": {"network": network},
            }

            if contract_address:
                request_params["tokenFilter"]["contractAddress"] = contract_address

            if token_id:
                request_params["tokenFilter"]["tokenId"] = token_id

            if owner_address:
                request_params["ownerFilter"] = {"address": owner_address}

            pagination_config = {
                "MaxItems": max_items,
                "PageSize": page_size,
                "StartingToken": starting_token,
            }

            response_iterator = paginator.paginate(**request_params, PaginationConfig=pagination_config)

            results = []
            for page in response_iterator:
                results.extend(page.get("tokenBalances", []))

            return results

        except botocore.exceptions.ClientError as e:
            print(f"Client error occurred: {e}")
            return {"error": str(e)}
        except botocore.exceptions.BotoCoreError as e:
            print(f"BotoCore error occurred: {e}")
            return {"error": str(e)}

    def paginate_list_transaction_events(
        self,
        network: str,
        transaction_hash: Optional[str] = None,
        transaction_id: Optional[str] = None,
        max_items: Optional[int] = None,
        page_size: Optional[int] = None,
        starting_token: Optional[str] = None
    ) -> List[Dict]:
        """
        Paginates through transaction events for a given transaction.

        :param network: The blockchain network (ETHEREUM_MAINNET, ETHEREUM_SEPOLIA_TESTNET, BITCOIN_MAINNET, BITCOIN_TESTNET).
        :param transaction_hash: (Optional) The hash of the transaction.
        :param transaction_id: (Optional) The identifier of a Bitcoin transaction (Only for Bitcoin networks).
        :param max_items: (Optional) The total number of items to return.
        :param page_size: (Optional) The size of each page.
        :param starting_token: (Optional) Token to specify where to start paginating.

        :return: List of transaction event details.
        """
        try:
            paginator = self.client.get_paginator("list_transaction_events")

            request_params = {
                "network": network,
            }

            if transaction_hash:
                request_params["transactionHash"] = transaction_hash

            if transaction_id:
                request_params["transactionId"] = transaction_id

            pagination_config = {
                "MaxItems": max_items,
                "PageSize": page_size,
                "StartingToken": starting_token,
            }

            response_iterator = paginator.paginate(**request_params, PaginationConfig=pagination_config)

            results = []
            for page in response_iterator:
                results.extend(page.get("events", []))

            return results

        except botocore.exceptions.ClientError as e:
            print(f"Client error occurred: {e}")
            return {"error": str(e)}
        except botocore.exceptions.BotoCoreError as e:
            print(f"BotoCore error occurred: {e}")
            return {"error": str(e)}

    def paginate_list_transactions(
        self,
        address: str,
        network: str,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        sort_order: Optional[str] = "ASCENDING",
        include_nonfinal: bool = False,
        max_items: Optional[int] = None,
        page_size: Optional[int] = None,
        starting_token: Optional[str] = None
    ) -> List[Dict]:
        """
        Paginates through transactions for a given address.

        :param address: (Required) The contract or wallet address whose transactions are requested.
        :param network: (Required) The blockchain network (ETHEREUM_MAINNET, ETHEREUM_SEPOLIA_TESTNET, BITCOIN_MAINNET, BITCOIN_TESTNET).
        :param from_time: (Optional) Start time for filtering transactions.
        :param to_time: (Optional) End time for filtering transactions.
        :param sort_order: (Optional) Sorting order (ASCENDING or DESCENDING). Default: ASCENDING.
        :param include_nonfinal: (Optional) Whether to include transactions that have not reached finality.
        :param max_items: (Optional) The total number of items to return.
        :param page_size: (Optional) The size of each page.
        :param starting_token: (Optional) Token to specify where to start paginating.

        :return: List of transactions.
        """
        try:
            paginator = self.client.get_paginator("list_transactions")

            request_params = {
                "address": address,
                "network": network,
                "sort": {"sortBy": "TRANSACTION_TIMESTAMP", "sortOrder": sort_order},
            }

            if from_time:
                request_params["fromBlockchainInstant"] = {"time": from_time}
            if to_time:
                request_params["toBlockchainInstant"] = {"time": to_time}
            if include_nonfinal:
                request_params["confirmationStatusFilter"] = {"include": ["FINAL", "NONFINAL"]}

            pagination_config = {
                "MaxItems": max_items,
                "PageSize": page_size,
                "StartingToken": starting_token,
            }

            response_iterator = paginator.paginate(**request_params, PaginationConfig=pagination_config)

            results = []
            for page in response_iterator:
                results.extend(page.get("transactions", []))

            return results

        except botocore.exceptions.ClientError as e:
            print(f"Client error occurred: {e}")
            return {"error": str(e)}
        except botocore.exceptions.BotoCoreError as e:
            print(f"BotoCore error occurred: {e}")
            return {"error": str(e)}

