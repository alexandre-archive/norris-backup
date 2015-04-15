#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED

def get_date():
    return datetime.today().strftime('%Y-%m-%d')

def compress_file(file_name, output_file):
    with ZipFile(output_file, 'w', ZIP_DEFLATED) as z:
        z.write(file_name)

    return output_file

def compress_folder(folder_name, output_file):
    with ZipFile(output_file, 'w', ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(folder_name):
            for f in files:
                z.write(os.path.join(root, f))

    return output_file

def upload_file(bucket, key, file_name):
    '''
    Upload a file to S3.
    '''
    conn = S3Connection()
    bucket = conn.get_bucket(bucket)
    k = Key(bucket)
    k.key = key
    k.set_contents_from_filename(file_name)

def db_dump(pwd, db, output_file):
    '''
    Dump Wordpress database (MySQL/MariaDB).
    '''
    os.popen('mysqldump -u root -p%s %s > %s' % (pwd, db, output_file))

def backup_db(pwd, db, bucket):
    '''
    Backup MySQL database and upload it to S3.
    '''
    date = get_date()
    file_name = 'db_backup_%s.sql' % date
    db_dump(pwd, db, file_name)
    file_name = compress_file(file_name, file_name + '.zip')
    upload_file(bucket, file_name, file_name)
    os.remove(file_name)

def backup_wp(wp_folder, bucket):
    '''
    Backup all WP folder and upload it to S3.
    '''
    date = get_date()
    file_name = 'wp_backup_%s.zip' % date
    file_name = compress_folder(wp_folder, file_name)
    upload_file(bucket, file_name, file_name)
    os.remove(file_name)

if __name__ == '__main__':
    try:
        import keys
    except ImportError:
        pass

    WP_ROOT_FOLDER = os.getenv('WP_ROOT_FOLDER', '')
    DB_ROOT_PWD = os.getenv('DB_ROOT_PWD', '')
    DB_WP_DB = os.getenv('DB_WP_DB', '')
    S3_WP_BUCKET = os.getenv('S3_WP_BUCKET', '')
    S3_DB_BUCKET = os.getenv('S3_DB_BUCKET', '')

    try:
        backup_wp(WP_ROOT_FOLDER, S3_WP_BUCKET)
    except Exception as e:
        print(e)

    try:
        backup_db(DB_ROOT_PWD, DB_WP_DB, S3_DB_BUCKET)
    except Exception as e:
        print(e)
