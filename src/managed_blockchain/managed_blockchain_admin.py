class ManagedBlockchainAdmin:
    def __init__(self):
        self.client = boto3.client("managedblockchain")

    def create_network(self, name, framework="HYPERLEDGER_FABRIC"):
        """Creates a new blockchain network."""
        response = self.client.create_network(
            Name=name,
            Framework=framework,
            FrameworkVersion="1.2",
            VotingPolicy={"ApprovalThresholdPolicy": {"ThresholdPercentage": 50}}
        )
        return response["NetworkId"]
