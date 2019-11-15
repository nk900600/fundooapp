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
from fundoo.settings import AWS_BUCKET
from botocore.exceptions import ClientError


class AmazoneS3:
    def upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:  # pragma: cover
            object_name = file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, AWS_BUCKET, object_name)
        except ClientError as error:
            logging.error(error)
            return False
        return response

    def delete(self, object_name):
        """delete a file to an S3 bucket
               :param object_name: S3 object name. If not specified then file_name is used
               :return: True if file was uploaded, else False
               """
        # If S3 object_name was not specified, use file_name
        s3_client = boto3.client('s3')
        try:
            response = s3_client.delete_object(Bucket=AWS_BUCKET, Key='image/' + object_name)
        except ClientError as error:
            logging.error(error)
            return False
        return response
    #
    # def wrap(self, func):
    #     def call(file_name,object_name, *sources):
    #         upload = self.upload_file( file_name, object_name)
    #         delete = self.delete(func)
    #         if shouldRebuild(cachefile, sources):
    #             result = func(*sources)
    #             fpickle(cachefile, result)
    #             self._cachefiles.append(cachefile)
    #         else:
    #             result = funpickle(cachefile)
    #         return result
    #
    #     return call
