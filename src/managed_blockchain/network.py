import boto3

class ManagedBlockchainNetwork:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def list_networks(self):
        """Lists all blockchain networks."""
        return self.client.list_networks()

    def get_network(self, network_id: str):
        """
        Retrieves detailed information about a specific blockchain network.

        :param network_id: The unique identifier of the network.
        :return: Dictionary containing network details or None if an error occurs.
        """
        try:
            response = self.client.get_network(NetworkId=network_id)
            return response.get("Network", {})
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

    def create_network(
        self,
        name: str,
        framework: str,
        framework_version: str,
        edition: str,
        voting_policy: dict,
        member_config: dict,
        description: str = "",
        tags: dict = None,
    ):
        """
        Creates a new blockchain network using Amazon Managed Blockchain.

        :param name: Name of the network.
        :param framework: The blockchain framework to use ('HYPERLEDGER_FABRIC' or 'ETHEREUM').
        :param framework_version: The version of the framework to use.
        :param edition: The edition of Managed Blockchain (for Hyperledger Fabric).
        :param voting_policy: The voting rules used to approve proposals.
        :param member_config: Configuration for the first member of the network.
        :param description: Optional description of the network.
        :param tags: Optional dictionary of tags.
        :return: Dictionary containing the NetworkId and MemberId.
        """
        try:
            response = self.client.create_network(
                ClientRequestToken=str(uuid.uuid4()),  # Ensures idempotency
                Name=name,
                Description=description,
                Framework=framework,
                FrameworkVersion=framework_version,
                FrameworkConfiguration={"Fabric": {"Edition": edition}},
                VotingPolicy={"ApprovalThresholdPolicy": voting_policy},
                MemberConfiguration=member_config,
                Tags=tags if tags else {},
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

    def delete_network(self, network_id: str):
        """Deletes a blockchain network."""
        return self.client.delete_network(NetworkId=network_id)
