import boto3
import botocore
from datetime import datetime
from typing import Optional, Dict, Any, List


class ManagedBlockchainQuery:
    def __init__(self):
        """Initialize the Managed Blockchain Query client."""
        self.client = boto3.client('managedblockchain-query')

    def batch_get_token_balance(self, token_requests: list):
        """
        Retrieves balances for multiple tokens for multiple owners in a single request.

        :param token_requests: List of dictionaries containing token and owner identifiers.
            Example:
            [
                {
                    "tokenIdentifier": {
                        "network": "ETHEREUM_MAINNET",
                        "contractAddress": "0x123...",
                        "tokenId": "1"
                    },
                    "ownerIdentifier": {
                        "address": "0xabc..."
                    },
                    "atBlockchainInstant": {
                        "time": datetime.utcnow()
                    }
                }
            ]
        :return: Dictionary containing token balances and errors (if any).
        """
        try:
            response = self.client.batch_get_token_balance(
                getTokenBalanceInputs=token_requests
            )
            return {
                "tokenBalances": response.get("tokenBalances", []),
                "errors": response.get("errors", [])
            }
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error fetching batch token balances: {e}")
            return {"tokenBalances": [], "errors": []}

    def get_asset_contract(self, network: str, contract_address: str):
        """
        Retrieve information about a specific blockchain contract.

        :param network: The blockchain network ('ETHEREUM_MAINNET', 'ETHEREUM_SEPOLIA_TESTNET', etc.).
        :param contract_address: The contract address on the blockchain.
        :return: Dictionary containing contract metadata.
        """
        try:
            response = self.client.get_asset_contract(
                contractIdentifier={
                    'network': network,
                    'contractAddress': contract_address
                }
            )
            return response
        except botocore.exceptions.ClientError as e:
            print(f"Error fetching contract details: {e}")
            return None

    def get_token_balance(self, network: str, owner_address: str, contract_address: Optional[str] = None,
                          token_id: Optional[str] = None, timestamp: Optional[datetime] = None) -> Dict:
        """
        Fetches the balance of a specific token for a given address on the blockchain.

        :param network: The blockchain network ('ETHEREUM_MAINNET', 'BITCOIN_MAINNET', etc.).
        :param owner_address: The contract or wallet address of the token owner.
        :param contract_address: (Optional) The contract address for the token.
        :param token_id: (Optional) The unique identifier of the token.
        :param timestamp: (Optional) The time at which to check the balance (defaults to latest).
        :return: Dictionary containing the token balance details.
        """
        try:
            token_identifier = {
                "network": network
            }
            if contract_address:
                token_identifier["contractAddress"] = contract_address
            if token_id:
                token_identifier["tokenId"] = token_id

            request_payload = {
                "tokenIdentifier": token_identifier,
                "ownerIdentifier": {
                    "address": owner_address
                }
            }
            if timestamp:
                request_payload["atBlockchainInstant"] = {"time": timestamp}

            response = self.client.get_token_balance(**request_payload)
            return response

        except botocore.exceptions.BotoCoreError as e:
            print(f"Error retrieving token balance: {e}")
            return {}

    def get_transaction(self, network: str, transaction_hash: Optional[str] = None,
                        transaction_id: Optional[str] = None) -> Dict:
        """
        Fetches the details of a blockchain transaction.

        :param network: The blockchain network ('ETHEREUM_MAINNET', 'BITCOIN_MAINNET', etc.).
        :param transaction_hash: The hash of the transaction (Ethereum & Bitcoin).
        :param transaction_id: The transaction ID (only for Bitcoin).
        :return: Dictionary containing the transaction details.
        """
        if not transaction_hash and not transaction_id:
            raise ValueError("Either transaction_hash or transaction_id must be provided.")

        try:
            request_payload = {
                "network": network
            }
            if transaction_hash:
                request_payload["transactionHash"] = transaction_hash
            if transaction_id and network in ["BITCOIN_MAINNET", "BITCOIN_TESTNET"]:
                request_payload["transactionId"] = transaction_id

            response = self.client.get_transaction(**request_payload)
            return response

        except botocore.exceptions.BotoCoreError as e:
            print(f"Error retrieving transaction details: {e}")
            return {}

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation supports pagination.

        :param operation_name: Name of the operation (e.g., 'list_transactions').
        :return: True if the operation supports pagination, False otherwise.
        """
        try:
            return self.client.can_paginate(operation_name)
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error checking pagination for {operation_name}: {e}")
            return False

    def close(self):
        """
        Closes the underlying endpoint connections.
        """
        try:
            self.client.close()
            print("Managed Blockchain Query client connection closed.")
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error closing client: {e}")

    def get_paginator(self, operation_name: str):
        """
        Create a paginator for a given Managed Blockchain Query operation.

        :param operation_name: The name of the operation (e.g., 'list_transactions').
        :return: A paginator object.
        """
        try:
            paginator = self.client.get_paginator(operation_name)
            return paginator
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error creating paginator: {e}")
            return None

    def get_waiter(self, waiter_name: str):
        """
        Returns an AWS Managed Blockchain Query Waiter.

        :param waiter_name: The name of the waiter to get.
        :return: The specified waiter object.
        """
        try:
            return self.client.get_waiter(waiter_name)
        except botocore.exceptions.WaiterError as e:
            print(f"Waiter error: {e}")
            return None

    def list_asset_contracts(
        self,
        network: str,
        token_standard: str,
        deployer_address: str,
        next_token: Optional[str] = None,
        max_results: int = 100
    ) -> Optional[Dict[str, Any]]:
        """
        Lists all asset contracts deployed by a specific address.

        :param network: The blockchain network (e.g., ETHEREUM_MAINNET, BITCOIN_MAINNET).
        :param token_standard: The token standard (e.g., ERC20, ERC721, ERC1155).
        :param deployer_address: The address that deployed the contract.
        :param next_token: The pagination token to fetch the next set of results.
        :param max_results: The maximum number of results to return (default: 100).
        :return: A dictionary containing contract details or None if an error occurs.
        """
        try:
            response = self.client.list_asset_contracts(
                contractFilter={
                    "network": network,
                    "tokenStandard": token_standard,
                    "deployerAddress": deployer_address
                },
                nextToken=next_token,
                maxResults=max_results
            )
            return response
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error communicating with AWS API: {e}")
            return None

    def list_filtered_transaction_events(
        self,
        network: str,
        transaction_event_to_address: List[str],
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        vout_spent: Optional[bool] = None,
        confirmation_status: Optional[List[str]] = None,
        sort_by: str = "blockchainInstant",
        sort_order: str = "ASCENDING",
        next_token: Optional[str] = None,
        max_results: int = 100
    ) -> Dict:
        """
        Lists all the transaction events for an address on the blockchain.

        :param network: The blockchain network (BITCOIN_MAINNET | BITCOIN_TESTNET).
        :param transaction_event_to_address: List of recipient addresses for filtering transactions.
        :param from_time: Start time for filtering transactions.
        :param to_time: End time for filtering transactions.
        :param vout_spent: Filter based on whether the transaction output is spent.
        :param confirmation_status: Filter transactions based on confirmation status (FINAL or NONFINAL).
        :param sort_by: Sorting criteria (default: "blockchainInstant").
        :param sort_order: Sorting order (ASCENDING or DESCENDING).
        :param next_token: Token for paginated results.
        :param max_results: Maximum number of results to return (default: 100).

        :return: Dictionary containing transaction events and metadata.
        """
        try:
            request_params = {
                "network": network,
                "addressIdentifierFilter": {"transactionEventToAddress": transaction_event_to_address},
                "sort": {"sortBy": sort_by, "sortOrder": sort_order},
                "maxResults": max_results
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

            if next_token:
                request_params["nextToken"] = next_token

            response = self.client.list_filtered_transaction_events(**request_params)
            return response

        except botocore.exceptions.ClientError as e:
            return {"error": str(e)}
        except botocore.exceptions.BotoCoreError as e:
            return {"error": str(e)}

    def list_token_balances(
        self,
        network: str,
        contract_address: Optional[str] = None,
        token_id: Optional[str] = None,
        owner_address: Optional[str] = None,
        next_token: Optional[str] = None,
        max_results: int = 100
    ) -> Dict:
        """
        Lists token balances for an address, contract, or specific token.

        :param network: The blockchain network (ETHEREUM_MAINNET, ETHEREUM_SEPOLIA_TESTNET, BITCOIN_MAINNET, BITCOIN_TESTNET).
        :param contract_address: (Optional) The contract address for filtering balances.
        :param token_id: (Optional) The unique identifier for a specific token.
        :param owner_address: (Optional) The wallet or contract address to check balances for.
        :param next_token: (Optional) Token for paginated results.
        :param max_results: Maximum number of results to return (default: 100).

        :return: Dictionary containing token balance details.
        """
        try:
            request_params = {
                "tokenFilter": {"network": network},
                "maxResults": max_results
            }

            if contract_address:
                request_params["tokenFilter"]["contractAddress"] = contract_address

            if token_id:
                request_params["tokenFilter"]["tokenId"] = token_id

            if owner_address:
                request_params["ownerFilter"] = {"address": owner_address}

            if next_token:
                request_params["nextToken"] = next_token

            response = self.client.list_token_balances(**request_params)
            return response

        except botocore.exceptions.ClientError as e:
            return {"error": str(e)}
        except botocore.exceptions.BotoCoreError as e:
            return {"error": str(e)}

    def list_transaction_events(
        self,
        network: str,
        transaction_hash: Optional[str] = None,
        transaction_id: Optional[str] = None,
        next_token: Optional[str] = None,
        max_results: int = 100
    ) -> Dict:
        """
        Lists all transaction events for a given transaction.

        :param network: The blockchain network (ETHEREUM_MAINNET, ETHEREUM_SEPOLIA_TESTNET, BITCOIN_MAINNET, BITCOIN_TESTNET).
        :param transaction_hash: (Optional) The hash of the transaction.
        :param transaction_id: (Optional) The identifier of a Bitcoin transaction (Only for Bitcoin networks).
        :param next_token: (Optional) Token for paginated results.
        :param max_results: Maximum number of results to return (default: 100).

        :return: Dictionary containing transaction event details.
        """
        try:
            request_params = {"network": network, "maxResults": max_results}

            if transaction_hash:
                request_params["transactionHash"] = transaction_hash
            if transaction_id:
                request_params["transactionId"] = transaction_id
            if next_token:
                request_params["nextToken"] = next_token

            response = self.client.list_transaction_events(**request_params)
            return response

        except botocore.exceptions.ClientError as e:
            return {"error": str(e)}
        except botocore.exceptions.BotoCoreError as e:
            return {"error": str(e)}

    def list_transactions(
        self,
        address: str,
        network: str,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        sort_order: Optional[str] = "ASCENDING",
        next_token: Optional[str] = None,
        max_results: int = 100,
        include_nonfinal: bool = False,
    ) -> Dict:
        """
        Lists all transactions for a given address.

        :param address: (Required) Contract or wallet address whose transactions are requested.
        :param network: (Required) Blockchain network (ETHEREUM_MAINNET, ETHEREUM_SEPOLIA_TESTNET, BITCOIN_MAINNET, BITCOIN_TESTNET).
        :param from_time: (Optional) Start time for transaction filtering (ISO 8601 format).
        :param to_time: (Optional) End time for transaction filtering (ISO 8601 format).
        :param sort_order: (Optional) Sorting order (ASCENDING or DESCENDING). Default: ASCENDING.
        :param next_token: (Optional) Token for paginated results.
        :param max_results: (Optional) Maximum number of results to return. Default: 100.
        :param include_nonfinal: (Optional) Whether to include transactions that have not reached finality.

        :return: Dictionary containing transaction details.
        """
        try:
            request_params = {
                "address": address,
                "network": network,
                "sort": {"sortBy": "TRANSACTION_TIMESTAMP", "sortOrder": sort_order},
                "maxResults": max_results,
            }

            if from_time:
                request_params["fromBlockchainInstant"] = {"time": from_time}
            if to_time:
                request_params["toBlockchainInstant"] = {"time": to_time}
            if next_token:
                request_params["nextToken"] = next_token
            if include_nonfinal:
                request_params["confirmationStatusFilter"] = {"include": ["FINAL", "NONFINAL"]}

            response = self.client.list_transactions(**request_params)
            return response

        except botocore.exceptions.ClientError as e:
            return {"error": str(e)}
        except botocore.exceptions.BotoCoreError as e:
            return {"error": str(e)}

