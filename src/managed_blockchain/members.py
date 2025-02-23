import boto3
import botocore
from typing import Optional, Dict, List


class ManagedBlockchainMembers:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def create_member(self, invitation_id: str, network_id: str, member_name: str, admin_username: str,
                      admin_password: str, description: str = None, tags: dict = None, kms_key_arn: str = None):
        """
        Creates a new member within a Managed Blockchain network.

        :param invitation_id: The unique identifier of the invitation sent to join the network.
        :param network_id: The unique identifier of the network where the member is created.
        :param member_name: Name of the new member.
        :param admin_username: Initial administrative user name for the member.
        :param admin_password: Password for the initial admin user.
        :param description: Optional description of the member.
        :param tags: Optional dictionary of key-value pairs for tagging.
        :param kms_key_arn: Optional KMS Key ARN for encryption at rest.
        :return: Dictionary containing the `MemberId` of the created member.
        """
        try:
            response = self.client.create_member(
                ClientRequestToken=str(uuid.uuid4()),  # Ensures idempotency
                InvitationId=invitation_id,
                NetworkId=network_id,
                MemberConfiguration={
                    'Name': member_name,
                    'Description': description or "",
                    'FrameworkConfiguration': {
                        'Fabric': {
                            'AdminUsername': admin_username,
                            'AdminPassword': admin_password
                        }
                    },
                    'LogPublishingConfiguration': {
                        'Fabric': {
                            'CaLogs': {
                                'Cloudwatch': {
                                    'Enabled': True
                                }
                            }
                        }
                    },
                    'Tags': tags if tags else {},
                    'KmsKeyArn': kms_key_arn or ""
                }
            )
            return response
        except self.client.exceptions.InvalidRequestException as e:
            print(f"Invalid request: {e}")
        except self.client.exceptions.AccessDeniedException as e:
            print(f"Access denied: {e}")
        except self.client.exceptions.ResourceNotFoundException as e:
            print(f"Resource not found: {e}")
        except self.client.exceptions.ResourceAlreadyExistsException as e:
            print(f"Member already exists: {e}")
        except self.client.exceptions.ResourceNotReadyException as e:
            print(f"Resource not ready: {e}")
        except self.client.exceptions.ThrottlingException as e:
            print(f"Throttling limit reached: {e}")
        except self.client.exceptions.ResourceLimitExceededException as e:
            print(f"Resource limit exceeded: {e}")
        except self.client.exceptions.InternalServiceErrorException as e:
            print(f"Internal service error: {e}")
        except self.client.exceptions.TooManyTagsException as e:
            print(f"Too many tags: {e}")

        return None

    def get_member(self, network_id: str, member_id: str):
        """
        Retrieves detailed information about a specific member.

        :param network_id: The unique identifier of the network to which the member belongs.
        :param member_id: The unique identifier of the member.
        :return: Dictionary containing member details or None if an error occurs.
        """
        try:
            response = self.client.get_member(NetworkId=network_id, MemberId=member_id)
            return response.get("Member", {})
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

    def list_members(
            self,
            network_id: str,
            name: Optional[str] = None,
            status: Optional[str] = None,
            is_owned: Optional[bool] = None,
            max_results: Optional[int] = None,
            next_token: Optional[str] = None
    ) -> Dict:
        """
        Retrieves a list of members in a specified network.

        :param network_id: The unique identifier of the network.
        :param name: Optional name filter for the member.
        :param status: Optional status filter (CREATING, AVAILABLE, etc.).
        :param is_owned: Optional filter for members owned by the AWS account.
        :param max_results: The maximum number of members to return.
        :param next_token: A pagination token for retrieving the next set of results.
        :return: A dictionary containing the list of members and the next pagination token.
        """
        try:
            params = {"NetworkId": network_id}
            if name:
                params["Name"] = name
            if status:
                params["Status"] = status
            if is_owned is not None:
                params["IsOwned"] = is_owned
            if max_results:
                params["MaxResults"] = max_results
            if next_token:
                params["NextToken"] = next_token

            response = self.client.list_members(**params)
            return response
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error listing members: {e}")
            return {}

    def get_all_members(self, network_id: str) -> List[Dict]:
        """
        Retrieves all members in a specified network, handling pagination.

        :param network_id: The unique identifier of the network.
        :return: A list of all members in the network.
        """
        members = []
        next_token = None

        while True:
            response = self.list_members(network_id=network_id, next_token=next_token)
            if 'Members' in response:
                members.extend(response['Members'])
            next_token = response.get('NextToken')
            if not next_token:
                break

        return members

    def delete_member(self, network_id: str, member_id: str):
        """
        Deletes a member from a specified network in AWS Managed Blockchain.

        :param network_id: The unique identifier of the network.
        :param member_id: The unique identifier of the member to remove.
        :return: None if successful, otherwise an error message.
        """
        try:
            response = self.client.delete_member(
                NetworkId=network_id,
                MemberId=member_id
            )
            print(f"Member {member_id} has been removed from network {network_id}.")
            return response
        except self.client.exceptions.InvalidRequestException as e:
            print(f"Invalid request: {e}")
        except self.client.exceptions.AccessDeniedException as e:
            print(f"Access denied: {e}")
        except self.client.exceptions.ResourceNotFoundException as e:
            print(f"Resource not found: {e}")
        except self.client.exceptions.ResourceNotReadyException as e:
            print(f"Resource not ready: {e}")
        except self.client.exceptions.ThrottlingException as e:
            print(f"Throttling limit reached: {e}")
        except self.client.exceptions.InternalServiceErrorException as e:
            print(f"Internal service error: {e}")

        return None

    def update_member(self, network_id: str, member_id: str, enable_logging: bool) -> bool:
        """
        Updates the member's log publishing configuration.

        :param network_id: The ID of the Managed Blockchain network.
        :param member_id: The ID of the member to update.
        :param enable_logging: Boolean flag to enable/disable CloudWatch logging.
        :return: True if the update is successful, False otherwise.
        """
        try:
            response = self.client.update_member(
                NetworkId=network_id,
                MemberId=member_id,
                LogPublishingConfiguration={
                    'Fabric': {
                        'CaLogs': {
                            'Cloudwatch': {
                                'Enabled': enable_logging
                            }
                        }
                    }
                }
            )
            print(f"Successfully updated member {member_id} in network {network_id}. Logging enabled: {enable_logging}")
            return True
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error updating member: {e}")
            return False
