"""
 ******************************************************************************
 *  Purpose: purpose is to store image to s3 bucket
 *
 *  @author  Nikhil Kumar
 *  @version 3.7
 *  @since   30/09/2019
 ******************************************************************************
"""

import logging
import boto3
from botocore.exceptions import ClientError


def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, 'django-s3-files', object_name)
    except ClientError as error:
        logging.error(error)
        return False
    return response
#
# s3_client = boto3.client('s3')
# s3_client.upload_file('/home/admin1/PycharmProjects/fundooapp/hello',
# 'django-s3-files', 'fidefdrstdcvdtupload')
