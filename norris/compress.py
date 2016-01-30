# -*- coding: utf-8 -*-

import logging
import os

from zipfile import ZipFile, ZIP_DEFLATED

logger = logging.getLogger(__name__)


class Compress(object):

    def compress_file(self, path, output_file):
        pass

    def compress_folder(self, path, output_file):
        pass

    @classmethod
    def get_compressor(cls, engine):
        if engine == 'zip':
            return ZipCompress()

        logger.info('Compress skypped. No compressors found for: %s' % engine)
        return Compress()


class ZipCompress(Compress):
    def compress_file(self, path, output_file):
        logger.info('Compressing (zip) file %s...' % path)

        with ZipFile(output_file, 'w', ZIP_DEFLATED) as z:
            z.write(path)

        logger.info('Compress done.')

    def compress_folder(self, path, output_file):
        logger.info('Compressing (zip) directory %s...' % path)

        with ZipFile(output_file, 'w', ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(path):
                for f in files:
                    z.write(os.path.join(root, f))

        logger.info('Compress done.')
