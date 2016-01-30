# -*- coding: utf-8 -*-

import logging
import os
import shutil
import sys
import unittest
import yaml

sys.path.append('./')
sys.path.append('./../')

from norris import compress
from norris import dump
from norris import norris

with open('./tests/logging.yml', 'r') as f:
    logging.config.dictConfig(yaml.load(f))


class TestDump(unittest.TestCase):

    def test_get_dumper(self):
        engine = dump.Dump.get_dumper('mariadb')
        self.assertTrue(isinstance(engine, dump.MySQLDump))
        engine = dump.Dump.get_dumper('mysql')
        self.assertTrue(isinstance(engine, dump.MySQLDump))

    def test_dump_mysql(self):
        engine = dump.MySQLDump()
        engine.dump_db('my-db', 'root', 'pwd', './tests/outputs/my-db.sql')
        self.assertTrue(os.path.exists('./tests/outputs/my-db.sql'))
        os.remove('./tests/outputs/my-db.sql')


class TestCompress(unittest.TestCase):

    def test_get_compressor(self):
        compressor = compress.Compress.get_compressor('zip')
        self.assertTrue(isinstance(compressor, compress.ZipCompress))

    def test_folder_zip_compress(self):
        compressor = compress.ZipCompress()
        compressor.compress_folder('./tests/assets/my-folder', './tests/outputs/my-folder.zip')
        self.assertTrue(os.path.exists('./tests/outputs/my-folder.zip'))
        os.remove('./tests/outputs/my-folder.zip')

    def test_file_zip_compress(self):
        compressor = compress.ZipCompress()
        compressor.compress_file('./tests/assets/my-file.txt', './tests/outputs/my-file.zip')
        self.assertTrue(os.path.exists('./tests/outputs/my-file.zip'))
        os.remove('./tests/outputs/my-file.zip')


class MockStorage(object):

    def upload_file(self, path, key):
        shutil.copy(path,  './tests/outputs/%s' % key)


def get_mock_storage(credential):
    return MockStorage()


class TestNorris(unittest.TestCase):

    def setUp(self):
        self._get_storage = norris.get_storage
        norris.get_storage = get_mock_storage

    def tearDown(self):
        norris.get_storage = self._get_storage

    def test_file_backup(self):
        norris.backup_file('./tests/assets/my-file.txt', 'my-file.txt', None)
        self.assertTrue(os.path.exists('./tests/outputs/my-file.txt'))
        os.remove('./tests/outputs/my-file.txt')

    # TODO: Can't upload folder without compress.
    # def test_folder_backup(self):
    #     norris.backup_folder('./tests/assets/my-folder', 'my-folder', None)
    #     self.assertTrue(os.path.exists('./tests/outputs/my-folder'))
    #     os.remove('./tests/outputs/my-folder')

    def test_db_backup(self):
        norris.backup_db('mysql', 'my-db', 'root', 'pwd', 'my-db.sql', None)
        self.assertTrue(os.path.exists('./tests/outputs/my-db.sql'))
        os.remove('./tests/outputs/my-db.sql')

    def test_file_backup_zip_compress(self):
        norris.backup_file('./tests/assets/my-file.txt', 'my-file.zip', 'zip')
        self.assertTrue(os.path.exists('./tests/outputs/my-file.zip'))
        os.remove('./tests/outputs/my-file.zip')

    def test_folder_backup_zip_compress(self):
        norris.backup_folder('./tests/assets/my-folder', 'my-folder.zip', 'zip')
        self.assertTrue(os.path.exists('./tests/outputs/my-folder.zip'))
        os.remove('./tests/outputs/my-folder.zip')

    def test_db_backup_zip_compress(self):
        norris.backup_db('mysql', 'my-db', 'root', 'pwd', 'my-db.zip', 'zip')
        self.assertTrue(os.path.exists('./tests/outputs/my-db.zip'))
        os.remove('./tests/outputs/my-db.zip')

if __name__ == '__main__':
    unittest.main()
