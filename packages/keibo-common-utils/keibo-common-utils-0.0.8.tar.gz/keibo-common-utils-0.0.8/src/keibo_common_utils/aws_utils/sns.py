import json
import boto3


def send_message_to_topic(topic_arn: str, subject: str, message: str):
    # Create a client object
    client = boto3.client("sns")

    # Publish message to SNS
    client.publish(
        TargetArn=topic_arn,
        Message=json.dumps({"default": json.dumps(message), "email": message}),
        MessageStructure="json",
        Subject=subject
    )
