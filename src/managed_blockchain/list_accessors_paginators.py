import boto3
import botocore
from datetime import datetime


class ManagedBlockchainPaginator:
    def __init__(self):
        """Initialize the Managed Blockchain client and paginator."""
        self.client = boto3.client('managedblockchain')
        self.paginator = self.client.get_paginator('list_accessors')

    def list_all_accessors(self, network_type: str, max_items: int = 100, page_size: int = 50):
        """
        Retrieves a paginated list of all accessors in the specified blockchain network.

        :param network_type: The blockchain network (ETHEREUM_MAINNET, POLYGON_MAINNET, etc.).
        :param max_items: Maximum total items to return.
        :param page_size: Number of items per page.
        :return: A list of accessor details.
        """
        accessors_list = []

        try:
            response_iterator = self.paginator.paginate(
                NetworkType=network_type,
                PaginationConfig={
                    'MaxItems': max_items,
                    'PageSize': page_size
                }
            )

            for page in response_iterator:
                for accessor in page.get('Accessors', []):
                    accessors_list.append({
                        "Id": accessor["Id"],
                        "Type": accessor["Type"],
                        "Status": accessor["Status"],
                        "CreationDate": accessor["CreationDate"].strftime('%Y-%m-%d %H:%M:%S'),
                        "Arn": accessor["Arn"],
                        "NetworkType": accessor["NetworkType"]
                    })

            print(f"Retrieved {len(accessors_list)} accessors for network {network_type}.")
            return accessors_list

        except botocore.exceptions.BotoCoreError as e:
            print(f"Error listing accessors: {e}")
            return []
