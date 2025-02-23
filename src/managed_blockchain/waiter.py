import boto3
import botocore

class ManagedBlockchainWaiter:
    def __init__(self):
        """Initialize the Managed Blockchain client."""
        self.client = boto3.client('managedblockchain')

    def wait_for_network_available(self, network_id: str, delay: int = 30, max_attempts: int = 20):
        """
        Waits for a network to become available.

        :param network_id: The unique identifier of the network.
        :param delay: The delay (in seconds) between attempts.
        :param max_attempts: The maximum number of polling attempts.
        :return: True if the network becomes available, False otherwise.
        """
        try:
            waiter = self.client.get_waiter('network_available')
            waiter.wait(
                NetworkId=network_id,
                WaiterConfig={'Delay': delay, 'MaxAttempts': max_attempts}
            )
            return True
        except botocore.exceptions.WaiterError as e:
            print(f"Error waiting for network {network_id} to become available: {e}")
        return False

    def wait_for_member_available(self, network_id: str, member_id: str, delay: int = 30, max_attempts: int = 20):
        """
        Waits for a member to become available in a network.

        :param network_id: The unique identifier of the network.
        :param member_id: The unique identifier of the member.
        :param delay: The delay (in seconds) between attempts.
        :param max_attempts: The maximum number of polling attempts.
        :return: True if the member becomes available, False otherwise.
        """
        try:
            waiter = self.client.get_waiter('member_available')
            waiter.wait(
                NetworkId=network_id,
                MemberId=member_id,
                WaiterConfig={'Delay': delay, 'MaxAttempts': max_attempts}
            )
            return True
        except botocore.exceptions.WaiterError as e:
            print(f"Error waiting for member {member_id} in network {network_id} to become available: {e}")
        return False

    def wait_for_node_available(self, network_id: str, member_id: str, node_id: str, delay: int = 30, max_attempts: int = 20):
        """
        Waits for a node to become available in a network.

        :param network_id: The unique identifier of the network.
        :param member_id: The unique identifier of the member.
        :param node_id: The unique identifier of the node.
        :param delay: The delay (in seconds) between attempts.
        :param max_attempts: The maximum number of polling attempts.
        :return: True if the node becomes available, False otherwise.
        """
        try:
            waiter = self.client.get_waiter('node_available')
            waiter.wait(
                NetworkId=network_id,
                MemberId=member_id,
                NodeId=node_id,
                WaiterConfig={'Delay': delay, 'MaxAttempts': max_attempts}
            )
            return True
        except botocore.exceptions.WaiterError as e:
            print(f"Error waiting for node {node_id} in network {network_id} to become available: {e}")
        return False
