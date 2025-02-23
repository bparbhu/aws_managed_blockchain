import boto3
import uuid
import botocore
from typing import Optional, Dict, List


class ManagedBlockchainAccessors:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def create_accessor(self, network_type: str, tags: dict = None):
        """
        Creates a new accessor for use with Amazon Managed Blockchain service.

        :param network_type: The blockchain network that the Accessor token is created for.
        :param tags: Optional dictionary of tags.
        :return: Dictionary containing the AccessorId and BillingToken.
        """
        try:
            response = self.client.create_accessor(
                ClientRequestToken=str(uuid.uuid4()),  # Ensures idempotency
                AccessorType="BILLING_TOKEN",
                Tags=tags if tags else {},
                NetworkType=network_type,
            )
            return response
        except self.client.exceptions.InvalidRequestException as e:
            print(f"Invalid request: {e}")
        except self.client.exceptions.AccessDeniedException as e:
            print(f"Access denied: {e}")
        except self.client.exceptions.ResourceAlreadyExistsException as e:
            print(f"Resource already exists: {e}")
        except self.client.exceptions.ThrottlingException as e:
            print(f"Throttling limit reached: {e}")
        except self.client.exceptions.ResourceLimitExceededException as e:
            print(f"Resource limit exceeded: {e}")
        except self.client.exceptions.InternalServiceErrorException as e:
            print(f"Internal service error: {e}")
        except self.client.exceptions.TooManyTagsException as e:
            print(f"Too many tags: {e}")

        return None

    def delete_accessor(self, accessor_id: str):
        """
        Deletes an accessor associated with an AWS Managed Blockchain account.

        :param accessor_id: The unique identifier of the accessor to delete.
        :return: None if successful, otherwise an error message.
        """
        try:
            response = self.client.delete_accessor(
                AccessorId=accessor_id
            )
            print(f"Accessor {accessor_id} has been marked for deletion.")
            return response
        except self.client.exceptions.InvalidRequestException as e:
            print(f"Invalid request: {e}")
        except self.client.exceptions.AccessDeniedException as e:
            print(f"Access denied: {e}")
        except self.client.exceptions.ResourceNotFoundException as e:
            print(f"Resource not found: {e}")
        except self.client.exceptions.ThrottlingException as e:
            print(f"Throttling limit reached: {e}")
        except self.client.exceptions.InternalServiceErrorException as e:
            print(f"Internal service error: {e}")

        return None

    def get_accessor(self, accessor_id: str):
        """
        Retrieves detailed information about a specific accessor.

        :param accessor_id: The unique identifier of the accessor.
        :return: Dictionary containing accessor details or None if an error occurs.
        """
        try:
            response = self.client.get_accessor(AccessorId=accessor_id)
            return response.get("Accessor", {})
        except self.client.exceptions.InvalidRequestException as e:
            print(f"Invalid request: {e}")
        except self.client.exceptions.AccessDeniedException as e:
            print(f"Access denied: {e}")
        except self.client.exceptions.ResourceNotFoundException as e:
            print(f"Resource not found: {e}")
        except self.client.exceptions.ThrottlingException as e:
            print(f"Throttling limit reached: {e}")
        except self.client.exceptions.InternalServiceErrorException as e:
            print(f"Internal service error: {e}")

        return None

    def list_accessors(
            self,
            max_results: Optional[int] = None,
            next_token: Optional[str] = None,
            network_type: Optional[str] = None
    ) -> Dict:
        """
        Retrieves a list of accessors and their properties.

        :param max_results: The maximum number of accessors to return.
        :param next_token: A pagination token for retrieving the next set of results.
        :param network_type: The blockchain network type for which accessors are created.
        :return: A dictionary containing the list of accessors and the next pagination token.
        """
        try:
            params = {}
            if max_results:
                params['MaxResults'] = max_results
            if next_token:
                params['NextToken'] = next_token
            if network_type:
                params['NetworkType'] = network_type

            response = self.client.list_accessors(**params)
            return response
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error listing accessors: {e}")
            return {}

    def get_all_accessors(self, network_type: Optional[str] = None) -> List[Dict]:
        """
        Retrieves all accessors available in Managed Blockchain, handling pagination.

        :param network_type: The blockchain network type for which accessors are created.
        :return: A list of all accessors.
        """
        accessors = []
        next_token = None

        while True:
            response = self.list_accessors(next_token=next_token, network_type=network_type)
            if 'Accessors' in response:
                accessors.extend(response['Accessors'])
            next_token = response.get('NextToken')
            if not next_token:
                break

        return accessors
