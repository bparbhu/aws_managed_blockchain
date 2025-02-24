import pytest
from unittest.mock import patch, MagicMock
import botocore
from datetime import datetime
import uuid

# Import all the modules from your project
from src.managed_blockchain.accessors import ManagedBlockchainAccessors
from src.managed_blockchain.invitations import ManagedBlockchainInvitations
from src.managed_blockchain.list_accessors_paginators import ManagedBlockchainPaginator
from src.managed_blockchain.managed_blockchain_admin import ManagedBlockchainAdmin
from src.managed_blockchain.members import ManagedBlockchainMembers
from src.managed_blockchain.network import ManagedBlockchainNetwork
from src.managed_blockchain.nodes import ManagedBlockchainNodes
from src.managed_blockchain.paginator import ManagedBlockchainPaginator
from src.managed_blockchain.proposals import ManagedBlockchainProposals
from src.managed_blockchain.tags import ManagedBlockchainTags
from src.managed_blockchain.waiter import ManagedBlockchainWaiter


@pytest.fixture
def mock_boto3_client():
    """Mock boto3 client for Managed Blockchain."""
    with patch("boto3.client") as mock_client:
        yield mock_client.return_value


# ---- Test Accessors ----
@pytest.fixture
def accessors_client(mock_boto3_client):
    return ManagedBlockchainAccessors()


def test_list_accessors(accessors_client, mock_boto3_client):
    mock_boto3_client.list_accessors.return_value = {"Accessors": [{"AccessorId": "acc-123"}]}
    response = accessors_client.list_accessors()
    assert response["Accessors"][0]["AccessorId"] == "acc-123"


# ---- Test Invitations ----
@pytest.fixture
def invitations_client(mock_boto3_client):
    return ManagedBlockchainInvitations()


def test_list_invitations(invitations_client, mock_boto3_client):
    mock_boto3_client.list_invitations.return_value = {"Invitations": [{"InvitationId": "inv-123"}]}
    response = invitations_client.list_invitations()
    assert response["Invitations"][0]["InvitationId"] == "inv-123"


# ---- Test Members ----
@pytest.fixture
def members_client(mock_boto3_client):
    return ManagedBlockchainMembers()


def test_create_member(members_client, mock_boto3_client):
    mock_boto3_client.create_member.return_value = {"MemberId": "m-123"}
    response = members_client.create_member(
        invitation_id="inv-123", network_id="n-456",
        member_name="TestMember", admin_username="admin",
        admin_password="password"
    )
    assert response["MemberId"] == "m-123"


def test_get_member(members_client, mock_boto3_client):
    mock_boto3_client.get_member.return_value = {"Member": {"MemberId": "m-123"}}
    response = members_client.get_member(network_id="n-123", member_id="m-123")
    assert response["Member"]["MemberId"] == "m-123"


# ---- Test Networks ----
@pytest.fixture
def network_client(mock_boto3_client):
    return ManagedBlockchainNetwork()


def test_list_networks(network_client, mock_boto3_client):
    mock_boto3_client.list_networks.return_value = {"Networks": [{"NetworkId": "n-123"}]}
    response = network_client.list_networks()
    assert response["Networks"][0]["NetworkId"] == "n-123"


# ---- Test Nodes ----
@pytest.fixture
def nodes_client(mock_boto3_client):
    return ManagedBlockchainNodes()


def test_list_nodes(nodes_client, mock_boto3_client):
    mock_boto3_client.list_nodes.return_value = {"Nodes": [{"NodeId": "nd-123"}]}
    response = nodes_client.list_nodes(network_id="n-123", member_id="m-456")
    assert response["Nodes"][0]["NodeId"] == "nd-123"


# ---- Test Tags ----
@pytest.fixture
def tags_client(mock_boto3_client):
    return ManagedBlockchainTags()


def test_list_tags(tags_client, mock_boto3_client):
    mock_boto3_client.list_tags_for_resource.return_value = {"Tags": {"Environment": "Test"}}
    response = tags_client.list_tags_for_resource(resource_arn="arn:aws:managedblockchain:::network/n-123")
    assert response["Tags"]["Environment"] == "Test"


# ---- Test Proposals ----
@pytest.fixture
def proposals_client(mock_boto3_client):
    return ManagedBlockchainProposals()


def test_create_proposal(proposals_client, mock_boto3_client):
    mock_boto3_client.create_proposal.return_value = {"ProposalId": "p-123"}
    response = proposals_client.create_proposal(network_id="n-123", member_id="m-456", actions={})
    assert response["ProposalId"] == "p-123"


# ---- Test Waiters ----
@pytest.fixture
def waiter_client(mock_boto3_client):
    return ManagedBlockchainWaiter()


def test_get_waiter(waiter_client, mock_boto3_client):
    mock_waiter = MagicMock()
    mock_boto3_client.get_waiter.return_value = mock_waiter
    waiter = waiter_client.get_waiter(waiter_name="network_available")
    assert waiter is not None


# ---- Test Paginators ----
@pytest.fixture
def paginator_client(mock_boto3_client):
    return ManagedBlockchainPaginator()


def test_list_networks_pagination(paginator_client, mock_boto3_client):
    mock_paginator = MagicMock()
    mock_boto3_client.get_paginator.return_value = mock_paginator
    mock_paginator.paginate.return_value = iter([
        {"Networks": [{"NetworkId": "n-123"}], "NextToken": "token1"},
        {"Networks": [{"NetworkId": "n-456"}], "NextToken": None}
    ])
    response = paginator_client.paginate_list_networks()
    assert response["Networks"][0]["NetworkId"] == "n-123"


# ---- Test Managed Blockchain Admin ----
@pytest.fixture
def admin_client(mock_boto3_client):
    return ManagedBlockchainAdmin()


def test_delete_member(admin_client, mock_boto3_client):
    mock_boto3_client.delete_member.return_value = {}
    response = admin_client.delete_member(network_id="n-123", member_id="m-456")
    assert response == {}


# ---- Error Handling ----
def test_get_member_invalid_id(members_client, mock_boto3_client):
    mock_boto3_client.get_member.side_effect = botocore.exceptions.ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "Member not found"}},
        "get_member"
    )
    response = members_client.get_member(network_id="n-123", member_id="invalid-id")
    assert response is None


# ---- Paginator: List Transactions ----
def test_list_transactions_pagination(paginator_client, mock_boto3_client):
    mock_paginator = MagicMock()
    mock_boto3_client.get_paginator.return_value = mock_paginator
    mock_paginator.paginate.return_value = iter([
        {"transactions": [{"transactionHash": "0xABC"}], "NextToken": "token1"},
        {"transactions": [{"transactionHash": "0xDEF"}], "NextToken": None}
    ])
    response = paginator_client.paginate_list_transactions(address="0x123", network="ETHEREUM_MAINNET")
    assert response["transactions"][0]["transactionHash"] == "0xABC"
