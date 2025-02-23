import boto3
import botocore
from typing import Dict, Optional

class ManagedBlockchainTags:
    def __init__(self):
        self.client = boto3.client('managedblockchain')

    def list_tags_for_resource(self, resource_arn: str) -> Dict[str, str]:
        """
        Retrieves a list of tags associated with a Managed Blockchain resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :return: A dictionary containing key-value pairs of tags.
        """
        try:
            response = self.client.list_tags_for_resource(ResourceArn=resource_arn)
            return response.get("Tags", {})
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error retrieving tags: {e}")
            return {}

    def print_tags(self, resource_arn: str):
        """
        Prints the tags of a resource in a user-friendly format.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        """
        tags = self.list_tags_for_resource(resource_arn)
        if not tags:
            print(f"No tags found for resource: {resource_arn}")
        else:
            print(f"Tags for {resource_arn}:")
            for key, value in tags.items():
                print(f"  {key}: {value}")

    def tag_resource(self, resource_arn: str, tags: dict) -> bool:
        """
        Adds or overwrites tags for a specified Managed Blockchain resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :param tags: A dictionary of tags to assign (key-value pairs).
        :return: True if tagging was successful, False otherwise.
        """
        try:
            self.client.tag_resource(ResourceArn=resource_arn, Tags=tags)
            print(f"Successfully tagged resource: {resource_arn} with tags: {tags}")
            return True
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error tagging resource: {e}")
            return False

    def untag_resource(self, resource_arn: str, tag_keys: list) -> bool:
        """
        Removes the specified tags from the Managed Blockchain resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :param tag_keys: A list of tag keys to remove.
        :return: True if untagging was successful, False otherwise.
        """
        try:
            self.client.untag_resource(ResourceArn=resource_arn, TagKeys=tag_keys)
            print(f"Successfully removed tags: {tag_keys} from resource: {resource_arn}")
            return True
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error removing tags: {e}")
            return False
