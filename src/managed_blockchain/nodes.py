import boto3
import uuid
class ManagedBlockchainNodes:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def create_node(
        self,
        network_id: str,
        instance_type: str,
        availability_zone: str = None,
        member_id: str = None,
        enable_chaincode_logs: bool = False,
        enable_peer_logs: bool = False,
        state_db: str = "CouchDB",
        tags: dict = None
    ):
        """
        Creates a new node in a Managed Blockchain network.

        :param network_id: The unique identifier of the blockchain network.
        :param instance_type: The AWS instance type for the node.
        :param availability_zone: The Availability Zone (required for Ethereum).
        :param member_id: The unique identifier of the member (required for Hyperledger Fabric).
        :param enable_chaincode_logs: Enable CloudWatch logs for chaincode execution (Hyperledger Fabric).
        :param enable_peer_logs: Enable CloudWatch logs for peer node actions (Hyperledger Fabric).
        :param state_db: The state database for Fabric nodes (LevelDB or CouchDB).
        :param tags: Optional dictionary of key-value pairs for tagging.
        :return: Dictionary containing the `NodeId` of the created node.
        """
        try:
            node_config = {
                'InstanceType': instance_type,
                'LogPublishingConfiguration': {
                    'Fabric': {
                        'ChaincodeLogs': {
                            'Cloudwatch': {'Enabled': enable_chaincode_logs}
                        },
                        'PeerLogs': {
                            'Cloudwatch': {'Enabled': enable_peer_logs}
                        }
                    }
                },
                'StateDB': state_db
            }

            # Add Availability Zone if it's an Ethereum network
            if availability_zone:
                node_config["AvailabilityZone"] = availability_zone

            response = self.client.create_node(
                ClientRequestToken=str(uuid.uuid4()),  # Ensures idempotency
                NetworkId=network_id,
                MemberId=member_id if member_id else "",
                NodeConfiguration=node_config,
                Tags=tags if tags else {}
            )

            return response
        except self.client.exceptions.InvalidRequestException as e:
            print(f"Invalid request: {e}")
        except self.client.exceptions.AccessDeniedException as e:
            print(f"Access denied: {e}")
        except self.client.exceptions.ResourceNotFoundException as e:
            print(f"Resource not found: {e}")
        except self.client.exceptions.ResourceAlreadyExistsException as e:
            print(f"Node already exists: {e}")
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

    def get_node(self, network_id: str, node_id: str, member_id: str = None):
        """
        Retrieves detailed information about a specific blockchain node.

        :param network_id: The unique identifier of the network.
        :param node_id: The unique identifier of the node.
        :param member_id: The unique identifier of the member (required for Hyperledger Fabric).
        :return: Dictionary containing node details or None if an error occurs.
        """
        try:
            params = {"NetworkId": network_id, "NodeId": node_id}
            if member_id:
                params["MemberId"] = member_id  # Required for Hyperledger Fabric

            response = self.client.get_node(**params)
            return response.get("Node", {})
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

    def list_nodes(self, network_id: str, member_id: str):
        """Lists all nodes in a blockchain network."""
        return self.client.list_nodes(NetworkId=network_id, MemberId=member_id)

    def delete_node(self, network_id: str, node_id: str, member_id: str = None):
        """
        Deletes a node from a specified blockchain network in AWS Managed Blockchain.

        :param network_id: The unique identifier of the network the node is on.
        :param node_id: The unique identifier of the node to remove.
        :param member_id: The unique identifier of the member (Required for Hyperledger Fabric).
        :return: None if successful, otherwise an error message.
        """
        try:
            params = {
                "NetworkId": network_id,
                "NodeId": node_id
            }
            if member_id:  # Required for Hyperledger Fabric
                params["MemberId"] = member_id

            response = self.client.delete_node(**params)
            print(f"Node {node_id} has been removed from network {network_id}.")
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

    def update_node(self, network_id: str, member_id: str, node_id: str, log_publishing_configuration: dict):
        """Updates a node's configuration."""
        return self.client.update_node(NetworkId=network_id, MemberId=member_id, NodeId=node_id, LogPublishingConfiguration=log_publishing_configuration)
