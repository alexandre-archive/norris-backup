# -*- coding: utf-8 -*-

import logging
import math
import os

from boto.s3.connection import S3Connection
from filechunkio import FileChunkIO

logger = logging.getLogger(__name__)

CHUNK_SIZE = 52428800  # 50 MiB


class S3Storage:

    def __init__(self, aws_key, aws_secret, aws_bucket, bucket_path):
        conn = S3Connection(aws_key, aws_secret)
        self.bucket = conn.get_bucket(aws_bucket)
        self.bucket_name = aws_bucket
        self.bucket_path = bucket_path

    def upload_file(self, path, key):
        '''
        Upload a file to S3.
        '''
        logger.info('Uploading file "%s" to bucket "%s"...' % (path, self.bucket_name))

        source_path = path
        source_size = os.stat(path).st_size
        s3_filename = os.path.join(self.bucket_path, key)
        mp = self.bucket.initiate_multipart_upload(s3_filename)

        try:
            chunk_count = int(math.ceil(source_size / float(CHUNK_SIZE)))
            # Send the file parts, using FileChunkIO to create a file-like object
            # that points to a certain byte range within the original file. We
            # set bytes to never exceed the original file size.
            for i in range(chunk_count):
                logger.info('Sending part %d of %d...' % (i + 1, chunk_count))
                offset = CHUNK_SIZE * i
                bytes = min(CHUNK_SIZE, source_size - offset)
                with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
                    mp.upload_part_from_file(fp, part_num=i + 1)

            mp.complete_upload()
            logger.info('Upload done.')
        except:
            mp.cancel_upload()
            logger.exception('Failed to upload file to S3: %s' % path)
