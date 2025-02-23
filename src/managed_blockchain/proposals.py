import boto3
import uuid
class ManagedBlockchainProposals:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def create_proposal(
        self,
        network_id: str,
        member_id: str,
        invitations: list = None,
        removals: list = None,
        description: str = "",
        tags: dict = None
    ):
        """
        Creates a proposal in a Managed Blockchain Hyperledger Fabric network.

        :param network_id: The unique identifier of the blockchain network.
        :param member_id: The unique identifier of the member creating the proposal.
        :param invitations: List of AWS account IDs to invite to the network.
        :param removals: List of member IDs to remove from the network.
        :param description: Description of the proposal (optional).
        :param tags: Optional dictionary of key-value pairs for tagging.
        :return: Dictionary containing the `ProposalId` of the created proposal.
        """
        try:
            actions = {}

            if invitations:
                actions["Invitations"] = [{"Principal": aws_id} for aws_id in invitations]

            if removals:
                actions["Removals"] = [{"MemberId": member_id} for member_id in removals]

            if not actions:
                raise ValueError("At least one action (invitations or removals) must be specified.")

            response = self.client.create_proposal(
                ClientRequestToken=str(uuid.uuid4()),  # Ensures idempotency
                NetworkId=network_id,
                MemberId=member_id,
                Actions=actions,
                Description=description,
                Tags=tags if tags else {}
            )

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
        except self.client.exceptions.TooManyTagsException as e:
            print(f"Too many tags: {e}")

        return None

    def get_proposal(self, network_id: str, proposal_id: str):
        """Retrieves details of a specific proposal."""
        return self.client.get_proposal(NetworkId=network_id, ProposalId=proposal_id)

    def list_proposals(self, network_id: str):
        """Lists all proposals for a blockchain network."""
        return self.client.list_proposals(NetworkId=network_id)

    def vote_on_proposal(self, network_id: str, proposal_id: str, voter_member_id: str, vote: str):
        """Votes on a proposal."""
        return self.client.vote_on_proposal(NetworkId=network_id, ProposalId=proposal_id, VoterMemberId=voter_member_id, Vote=vote)
