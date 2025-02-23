import boto3

class ManagedBlockchainInvitations:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def list_invitations(self):
        """Lists invitations to join a blockchain network."""
        return self.client.list_invitations()

    def reject_invitation(self, invitation_id: str):
        """Rejects an invitation to join a blockchain network."""
        return self.client.reject_invitation(InvitationId=invitation_id)
