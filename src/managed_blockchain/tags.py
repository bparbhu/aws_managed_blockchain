import boto3

class ManagedBlockchainTags:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def list_tags_for_resource(self, resource_arn: str):
        """Lists all tags for a blockchain resource."""
        return self.client.list_tags_for_resource(ResourceArn=resource_arn)

    def tag_resource(self, resource_arn: str, tags: dict):
        """Adds tags to a blockchain resource."""
        return self.client.tag_resource(ResourceArn=resource_arn, Tags=tags)

    def untag_resource(self, resource_arn: str, tag_keys: list):
        """Removes tags from a blockchain resource."""
        return self.client.untag_resource(ResourceArn=resource_arn, TagKeys=tag_keys)
