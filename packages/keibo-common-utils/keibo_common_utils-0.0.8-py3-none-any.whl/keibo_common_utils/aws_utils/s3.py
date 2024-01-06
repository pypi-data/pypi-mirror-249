import os
import boto3
import pathlib
from botocore.exceptions import ClientError
from keibo_common_utils.logging_utils.p_logger import P_Logger


def upload_file(file_name: str, bucket: str, logger: P_Logger, object_name: str = None) -> bool:
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file to S3
    s3_client = boto3.client("s3")

    try:
        logger.info(f"Uploading file {file_name} to S3")
        s3_client.upload_file(file_name, bucket, object_name)
        logger.info(f"{file_name} uploaded successfully to S3")
    except ClientError as e:
        logger.error(e)

        return False

    return True

def download_file(bucket: str, logger: P_Logger, object_name: str, output_folder: str) -> bool:
    # Create s3 client
    s3_client = boto3.client("s3")

    # Initialize variables
    file_name = os.path.basename(object_name)
    output_path = os.path.join(output_folder, file_name)

    try:
        logger.info(f"Downloading file {object_name} from S3")
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
        s3_client.download_file(bucket, object_name, output_path)
        logger.info(f"{object_name} downloaded successfully from S3")
    except ClientError as e:
        logger.error(e)

        return False

    return True
