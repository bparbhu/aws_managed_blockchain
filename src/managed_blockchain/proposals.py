import boto3
import uuid
import botocore
from typing import Optional, Dict, List


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
        """
        Retrieves detailed information about a specific proposal.

        :param network_id: The unique identifier of the network for which the proposal is made.
        :param proposal_id: The unique identifier of the proposal.
        :return: Dictionary containing proposal details or None if an error occurs.
        """
        try:
            response = self.client.get_proposal(NetworkId=network_id, ProposalId=proposal_id)
            return response.get("Proposal", {})
        except botocore.exceptions.ClientError as e:
            print(f"Error retrieving proposal {proposal_id}: {e}")
        return None

    def list_proposals(
        self,
        network_id: str,
        max_results: Optional[int] = None,
        next_token: Optional[str] = None
    ) -> Dict:
        """
        Retrieves a list of proposals for the specified network.

        :param network_id: The unique identifier of the network.
        :param max_results: The maximum number of proposals to return.
        :param next_token: A pagination token for retrieving the next set of results.
        :return: A dictionary containing the list of proposals and the next pagination token.
        """
        try:
            params = {"NetworkId": network_id}
            if max_results:
                params["MaxResults"] = max_results
            if next_token:
                params["NextToken"] = next_token

            response = self.client.list_proposals(**params)
            return response
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error listing proposals: {e}")
            return {}

    def get_all_proposals(self, network_id: str) -> List[Dict]:
        """
        Retrieves all proposals for a network, handling pagination.

        :param network_id: The unique identifier of the network.
        :return: A list of all proposals.
        """
        proposals = []
        next_token = None

        while True:
            response = self.list_proposals(network_id=network_id, next_token=next_token)
            if 'Proposals' in response:
                proposals.extend(response['Proposals'])
            next_token = response.get('NextToken')
            if not next_token:
                break

        return proposals

    def filter_proposals_by_status(self, network_id: str, status: str) -> List[Dict]:
        """
        Retrieves all proposals for a network and filters by status.

        :param network_id: The unique identifier of the network.
        :param status: The status to filter proposals by.
                       Options: 'IN_PROGRESS', 'APPROVED', 'REJECTED', 'EXPIRED', 'ACTION_FAILED'
        :return: A list of proposals matching the specified status.
        """
        all_proposals = self.get_all_proposals(network_id)
        return [proposal for proposal in all_proposals if proposal.get("Status") == status]

    def vote_on_proposal(self, network_id: str, proposal_id: str, voter_member_id: str, vote: str) -> bool:
        """
        Casts a vote on a proposal.

        :param network_id: The unique identifier of the network.
        :param proposal_id: The unique identifier of the proposal.
        :param voter_member_id: The unique identifier of the member casting the vote.
        :param vote: The value of the vote ('YES' or 'NO').
        :return: True if the vote is successful, False otherwise.
        """
        if vote not in ["YES", "NO"]:
            print("Invalid vote value. Vote must be 'YES' or 'NO'.")
            return False

        try:
            self.client.vote_on_proposal(
                NetworkId=network_id,
                ProposalId=proposal_id,
                VoterMemberId=voter_member_id,
                Vote=vote
            )
            print(
                f"Successfully cast {vote} vote on proposal {proposal_id} in network {network_id} as member {voter_member_id}.")
            return True
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error voting on proposal: {e}")
            return False

    def list_proposal_votes(
            self,
            network_id: str,
            proposal_id: str,
            max_results: Optional[int] = None,
            next_token: Optional[str] = None
    ) -> Dict:
        """
        Retrieves a list of votes for a specified proposal.

        :param network_id: The unique identifier of the network.
        :param proposal_id: The unique identifier of the proposal.
        :param max_results: The maximum number of votes to return.
        :param next_token: A pagination token for retrieving the next set of results.
        :return: A dictionary containing the list of votes and the next pagination token.
        """
        try:
            params = {"NetworkId": network_id, "ProposalId": proposal_id}
            if max_results:
                params["MaxResults"] = max_results
            if next_token:
                params["NextToken"] = next_token

            response = self.client.list_proposal_votes(**params)
            return response
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error listing proposal votes: {e}")
            return {}

    def get_all_proposal_votes(self, network_id: str, proposal_id: str) -> List[Dict]:
        """
        Retrieves all votes for a specified proposal, handling pagination.

        :param network_id: The unique identifier of the network.
        :param proposal_id: The unique identifier of the proposal.
        :return: A list of all votes cast for the proposal.
        """
        votes = []
        next_token = None

        while True:
            response = self.list_proposal_votes(network_id=network_id, proposal_id=proposal_id, next_token=next_token)
            if 'ProposalVotes' in response:
                votes.extend(response['ProposalVotes'])
            next_token = response.get('NextToken')
            if not next_token:
                break

        return votes