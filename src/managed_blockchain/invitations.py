import boto3
import botocore
from typing import Optional, Dict, List
class ManagedBlockchainInvitations:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def list_invitations(self, max_results: Optional[int] = None, next_token: Optional[str] = None) -> Dict:
        """
        Retrieves a list of all invitations for the current AWS account.

        :param max_results: The maximum number of invitations to return.
        :param next_token: A pagination token for retrieving the next set of results.
        :return: A dictionary containing the list of invitations and the next pagination token.
        """
        try:
            params = {}
            if max_results:
                params['MaxResults'] = max_results
            if next_token:
                params['NextToken'] = next_token

            response = self.client.list_invitations(**params)
            return response
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error listing invitations: {e}")
            return {}

    def get_all_invitations(self) -> List[Dict]:
        """
        Retrieves all invitations available in Managed Blockchain, handling pagination.

        :return: A list of all invitations.
        """
        invitations = []
        next_token = None

        while True:
            response = self.list_invitations(next_token=next_token)
            if 'Invitations' in response:
                invitations.extend(response['Invitations'])
            next_token = response.get('NextToken')
            if not next_token:
                break

        return invitations

    def reject_invitation(self, invitation_id: str) -> bool:
        """
        Rejects an invitation to join a Managed Blockchain network.

        :param invitation_id: The unique identifier of the invitation to reject.
        :return: True if the invitation was successfully rejected, False otherwise.
        """
        try:
            self.client.reject_invitation(InvitationId=invitation_id)
            print(f"Successfully rejected invitation: {invitation_id}")
            return True
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error rejecting invitation: {e}")
            return False
