import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()

# AWS Credentials
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# AWS Managed Blockchain Configuration
BLOCKCHAIN_NETWORK = os.getenv("BLOCKCHAIN_NETWORK", "ETHEREUM_MAINNET")

# AWS Clients
def get_managed_blockchain_client():
    """Returns a boto3 client for AWS Managed Blockchain."""
    return boto3.client(
        "managedblockchain",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

def get_managed_blockchain_query_client():
    """Returns a boto3 client for AWS Managed Blockchain Query."""
    return boto3.client(
        "managedblockchain-query",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
