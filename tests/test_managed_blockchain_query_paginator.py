import pytest
from unittest.mock import patch, MagicMock
import botocore
from datetime import datetime
from src.managed_blockchain_query.managed_blockchain_paginator import ManagedBlockchainPaginator


@pytest.fixture
def mock_boto3_client():
    """Mock boto3 client for ManagedBlockchainPaginator."""
    with patch("boto3.client") as mock_client:
        yield mock_client.return_value


@pytest.fixture
def paginator_client(mock_boto3_client):
    """Return an instance of ManagedBlockchainPaginator with a mocked client."""
    return ManagedBlockchainPaginator()


### ✅ TEST: Paginate Chaincode Queries on Hyperledger Fabric
def test_paginate_chaincode_queries(paginator_client, mock_boto3_client):
    mock_paginator = MagicMock()
    mock_boto3_client.get_paginator.return_value = mock_paginator

    mock_paginator.paginate.return_value = iter([
        {"transactions": [{"transactionId": "txABC"}], "NextToken": "token1"},
        {"transactions": [{"transactionId": "txDEF"}], "NextToken": None}
    ])

    response = paginator_client.paginate_list_transactions(
        address="Org1MSP",
        network="HYPERLEDGER_FABRIC",
        max_items=10,
        page_size=5
    )

    assert len(response) == 2
    assert response[0]["transactionId"] == "txABC"
    assert response[1]["transactionId"] == "txDEF"


### ✅ TEST: Paginate Smart Contract Deployments on Hyperledger Fabric
def test_paginate_chaincode_deployments(paginator_client, mock_boto3_client):
    mock_paginator = MagicMock()
    mock_boto3_client.get_paginator.return_value = mock_paginator

    mock_paginator.paginate.return_value = iter([
        {"contracts": [{"chaincodeId": "fabcar", "version": "1.0"}], "NextToken": "token1"},
        {"contracts": [{"chaincodeId": "supplychain", "version": "2.0"}], "NextToken": None}
    ])

    response = paginator_client.paginate_list_asset_contracts(
        network="HYPERLEDGER_FABRIC",
        token_standard="chaincode",
        deployer_address="Org1MSP"
    )

    assert len(response) == 2
    assert response[0]["chaincodeId"] == "fabcar"
    assert response[1]["chaincodeId"] == "supplychain"


### ✅ TEST: Paginate Transaction Events on Hyperledger Fabric
def test_paginate_transaction_events(paginator_client, mock_boto3_client):
    mock_paginator = MagicMock()
    mock_boto3_client.get_paginator.return_value = mock_paginator

    mock_paginator.paginate.return_value = iter([
        {"events": [{"transactionId": "tx123", "eventType": "Invoke"}], "NextToken": "token1"},
        {"events": [{"transactionId": "tx456", "eventType": "Query"}], "NextToken": None}
    ])

    response = paginator_client.paginate_list_transaction_events(
        network="HYPERLEDGER_FABRIC",
        transaction_hash="tx12345"
    )

    assert len(response) == 2
    assert response[0]["transactionId"] == "tx123"
    assert response[0]["eventType"] == "Invoke"
    assert response[1]["transactionId"] == "tx456"
    assert response[1]["eventType"] == "Query"


### ✅ TEST: Paginate Ledger Queries on Hyperledger Fabric
def test_paginate_ledger_queries(paginator_client, mock_boto3_client):
    mock_paginator = MagicMock()
    mock_boto3_client.get_paginator.return_value = mock_paginator

    mock_paginator.paginate.return_value = iter([
        {"ledgerState": [{"blockNumber": 10, "status": "VALID"}], "NextToken": "token1"},
        {"ledgerState": [{"blockNumber": 20, "status": "VALID"}], "NextToken": None}
    ])

    response = paginator_client.paginate_list_filtered_transaction_events(
        network="HYPERLEDGER_FABRIC",
        transaction_event_to_address=["Org1MSP"]
    )

    assert len(response) == 2
    assert response[0]["blockNumber"] == 10
    assert response[1]["blockNumber"] == 20


### ✅ TEST: Paginate Token Balances on Hyperledger Fabric
def test_paginate_token_balances(paginator_client, mock_boto3_client):
    mock_paginator = MagicMock()
    mock_boto3_client.get_paginator.return_value = mock_paginator

    mock_paginator.paginate.return_value = iter([
        {"tokenBalances": [{"ownerIdentifier": {"address": "Org1MSP"}, "balance": "100"}], "NextToken": "token1"},
        {"tokenBalances": [{"ownerIdentifier": {"address": "Org2MSP"}, "balance": "250"}], "NextToken": None}
    ])

    response = paginator_client.paginate_list_token_balances(
        network="HYPERLEDGER_FABRIC",
        owner_address="Org1MSP"
    )

    assert len(response) == 2
    assert response[0]["ownerIdentifier"]["address"] == "Org1MSP"
    assert response[0]["balance"] == "100"
    assert response[1]["ownerIdentifier"]["address"] == "Org2MSP"
    assert response[1]["balance"] == "250"


### ✅ TEST: Paginate Chaincode Invocation Transactions
def test_paginate_chaincode_invocation_transactions(paginator_client, mock_boto3_client):
    mock_paginator = MagicMock()
    mock_boto3_client.get_paginator.return_value = mock_paginator

    mock_paginator.paginate.return_value = iter([
        {"transactions": [{"transactionId": "txInvoke1", "type": "Invoke"}], "NextToken": "token1"},
        {"transactions": [{"transactionId": "txInvoke2", "type": "Invoke"}], "NextToken": None}
    ])

    response = paginator_client.paginate_list_transactions(
        address="Org1MSP",
        network="HYPERLEDGER_FABRIC",
        max_items=10
    )

    assert len(response) == 2
    assert response[0]["transactionId"] == "txInvoke1"
    assert response[0]["type"] == "Invoke"
    assert response[1]["transactionId"] == "txInvoke2"
    assert response[1]["type"] == "Invoke"


### ✅ TEST: Paginate Errors Properly Handled
def test_pagination_error_handling(paginator_client, mock_boto3_client):
    mock_boto3_client.get_paginator.side_effect = botocore.exceptions.ClientError(
        {"Error": {"Code": "ValidationException", "Message": "Invalid request"}},
        "get_paginator"
    )

    response = paginator_client.paginate_list_transactions(
        address="Org1MSP",
        network="HYPERLEDGER_FABRIC"
    )

    assert "error" in response
    assert "ValidationException" in response["error"]
