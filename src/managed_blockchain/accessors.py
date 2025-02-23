import boto3
import uuid
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

    def list_accessors(self, network_type: str, max_items: int = 100, page_size: int = 50, starting_token: str = None):
        """
        Lists all accessors in the blockchain network with pagination.

        :param network_type: The blockchain network type.
        :param max_items: The maximum number of items to return.
        :param page_size: The number of results per page.
        :param starting_token: A token to start pagination.
        :return: A list of accessors with their metadata.
        """
        paginator: Paginator = self.client.get_paginator('list_accessors')

        pagination_config = {
            "MaxItems": max_items,
            "PageSize": page_size
        }

        if starting_token:
            pagination_config["StartingToken"] = starting_token

        response_iterator = paginator.paginate(
            NetworkType=network_type,
            PaginationConfig=pagination_config
        )

        accessors_list = []
        for page in response_iterator:
            accessors_list.extend(page.get("Accessors", []))

        return accessors_list
