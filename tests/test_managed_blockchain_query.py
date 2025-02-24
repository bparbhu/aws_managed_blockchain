import pytest
from unittest.mock import patch, MagicMock
import botocore
from datetime import datetime
from src.managed_blockchain_query.managed_blockchain_query import ManagedBlockchainQuery

@pytest.fixture
def mock_boto3_client():
    """Mock boto3 client for ManagedBlockchainQuery."""
    with patch("boto3.client") as mock_client:
        yield mock_client.return_value

@pytest.fixture
def blockchain_client(mock_boto3_client):
    """Return an instance of ManagedBlockchainQuery with a mocked client."""
    return ManagedBlockchainQuery()


### ✅ TEST: Query Chaincode on Hyperledger Fabric
def test_query_chaincode(blockchain_client, mock_boto3_client):
    mock_boto3_client.invoke_chaincode.return_value = {
        "payload": "Query result from chaincode"
    }

    response = blockchain_client.invoke_chaincode(
        network="HYPERLEDGER_FABRIC",
        channel_name="mychannel",
        chaincode_id="fabcar",
        function="queryCar",
        args=["CAR4"]
    )

    assert response["payload"] == "Query result from chaincode"


### ✅ TEST: Invoke Chaincode on Hyperledger Fabric
def test_invoke_chaincode(blockchain_client, mock_boto3_client):
    mock_boto3_client.invoke_chaincode.return_value = {
        "transactionId": "tx123456789"
    }

    response = blockchain_client.invoke_chaincode(
        network="HYPERLEDGER_FABRIC",
        channel_name="mychannel",
        chaincode_id="fabcar",
        function="createCar",
        args=["CAR10", "Toyota", "Camry", "White", "Tom"]
    )

    assert response["transactionId"] == "tx123456789"


### ✅ TEST: Get Ledger State on Hyperledger Fabric
def test_get_ledger_state(blockchain_client, mock_boto3_client):
    mock_boto3_client.get_ledger_state.return_value = {
        "state": "VALID"
    }

    response = blockchain_client.get_ledger_state(
        network="HYPERLEDGER_FABRIC",
        channel_name="mychannel",
        block_number=100
    )

    assert response["state"] == "VALID"


### ✅ TEST: Fetch Contract Details (Smart Contract in Hyperledger Fabric)
def test_get_chaincode_info(blockchain_client, mock_boto3_client):
    mock_boto3_client.get_chaincode_info.return_value = {
        "chaincodeId": "fabcar",
        "version": "1.0",
        "endorsementPolicy": "Org1 & Org2"
    }

    response = blockchain_client.get_chaincode_info(
        network="HYPERLEDGER_FABRIC",
        channel_name="mychannel",
        chaincode_id="fabcar"
    )

    assert response["chaincodeId"] == "fabcar"
    assert response["version"] == "1.0"
    assert response["endorsementPolicy"] == "Org1 & Org2"


### ✅ TEST: Pagination for Transactions
def test_list_hyperledger_transactions_pagination(blockchain_client, mock_boto3_client):
    mock_paginator = MagicMock()
    mock_boto3_client.get_paginator.return_value = mock_paginator

    # Simulating multiple pages
    mock_paginator.paginate.return_value = iter([
        {"transactions": [{"transactionId": "txABC"}], "NextToken": "token1"},
        {"transactions": [{"transactionId": "txDEF"}], "NextToken": None}
    ])

    response = blockchain_client.list_transactions(
        address="Org1MSP",
        network="HYPERLEDGER_FABRIC"
    )

    assert len(response["transactions"]) == 2
    assert response["transactions"][0]["transactionId"] == "txABC"
    assert response["transactions"][1]["transactionId"] == "txDEF"


### ✅ TEST: Error Handling for Transactions
def test_list_hyperledger_transactions_error_handling(blockchain_client, mock_boto3_client):
    mock_boto3_client.list_transactions.side_effect = botocore.exceptions.ClientError(
        {"Error": {"Code": "ValidationException", "Message": "Invalid request"}},
        "list_transactions"
    )

    response = blockchain_client.list_transactions(
        address="Org1MSP",
        network="HYPERLEDGER_FABRIC"
    )

    assert "error" in response
    assert "ValidationException" in response["error"]


### ✅ TEST: Ledger Info Retrieval
def test_get_ledger_info(blockchain_client, mock_boto3_client):
    mock_boto3_client.get_ledger_info.return_value = {
        "ledgerName": "test-ledger",
        "state": "ACTIVE"
    }

    response = blockchain_client.get_ledger_info(
        network="HYPERLEDGER_FABRIC",
        ledger_name="test-ledger"
    )

    assert response["ledgerName"] == "test-ledger"
    assert response["state"] == "ACTIVE"


### ✅ TEST: Hyperledger Fabric Block Retrieval
def test_get_block(blockchain_client, mock_boto3_client):
    mock_boto3_client.get_block.return_value = {
        "blockNumber": 100,
        "blockHash": "0xabc123",
        "previousBlockHash": "0xdef456"
    }

    response = blockchain_client.get_block(
        network="HYPERLEDGER_FABRIC",
        channel_name="mychannel",
        block_number=100
    )

    assert response["blockNumber"] == 100
    assert response["blockHash"] == "0xabc123"
    assert response["previousBlockHash"] == "0xdef456"
