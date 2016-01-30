#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import os
import requests
import yaml

from datetime import datetime

from .compress import Compress
from .dump import Dump
from .storage import S3Storage

logger = logging.getLogger('norris')


def safe(func):
    def func_wrapper(*args, **kwargs):
        try:
            logger.info('Backup started.')
            func(*args, **kwargs)
            logger.info('Backup done.')
        except Exception as e:
            logger.exception(e)

    return func_wrapper


def value_or_raise(l, key):
    if key in l:
        return l[key]

    raise KeyError('Key not found: %s' % key)


def get_file_name(format):
    return datetime.today().strftime(format)


def get_storage(credential):
    aws_key = value_or_raise(credential, 'key')
    aws_secret = value_or_raise(credential, 'secret')
    bucket = value_or_raise(credential, 'bucket')
    aws_bucket = value_or_raise(bucket, 'name')
    bucket_path = value_or_raise(bucket, 'path')
    return S3Storage(aws_key, aws_secret, aws_bucket, bucket_path)


@safe
def backup_folder(path, output_path, compressor, aws_credential=None):
    '''
    Backup a folder and upload it to S3.
    '''
    if not os.path.isdir(path):
        raise IOError('%s must be a directory.' % path)

    if compressor:
        output_file = get_file_name(output_path)
        Compress.get_compressor(compressor).compress_folder(path, output_file)
        get_storage(aws_credential).upload_file(output_file, output_file)
        os.remove(output_file)
    else:
        logger.info('Skipping folder backup due to no compressor found.')


@safe
def backup_file(path, output_path, compressor, aws_credential=None):
    '''
    Backup a file and upload it to S3.
    '''
    if not os.path.isfile(path):
        raise IOError('%s must be a file.' % path)

    output_file = get_file_name(output_path)

    if compressor:
        Compress.get_compressor(compressor).compress_file(path, output_file)
        get_storage(aws_credential).upload_file(output_file, output_file)
        os.remove(output_file)
    else:
        get_storage(aws_credential).upload_file(path, output_file)


@safe
def backup_db(engine, db, user, pwd, output_path, compressor, aws_credential=None):
    '''
    Backup a database and upload it to S3.
    '''
    dump_file = 'dump_%s.sql' % db
    Dump.get_dumper(engine).dump_db(user, pwd, db, dump_file)
    output_file = get_file_name(output_path)

    if compressor:
        Compress.get_compressor(compressor).compress_file(dump_file, output_file)
        get_storage(aws_credential).upload_file(output_file, output_file)
        os.remove(output_file)
    else:
        get_storage(aws_credential).upload_file(dump_file, output_file)

    os.remove(dump_file)


def backup(backup_cfg, aws_credentials):
    for credential_key, backup_list in backup_cfg.items():
        aws_credential = value_or_raise(aws_credentials, credential_key)

        for cfg in backup_list:
            backup_type = value_or_raise(cfg, 'type')
            output_path = value_or_raise(cfg, 'output_path')

            if cfg.get('compress', False):
                compressor = cfg.get('compressor', 'zip')
            else:
                compressor = None

            if backup_type == 'dir':
                path = value_or_raise(cfg, 'path')
                backup_folder(path, output_path, compressor, aws_credential)
            elif backup_type == 'file':
                path = value_or_raise(cfg, 'path')
                backup_file(path, output_path, compressor, aws_credential)
            elif backup_type == 'db':
                engine = value_or_raise(cfg, 'engine')
                db = value_or_raise(cfg, 'database')
                user = value_or_raise(cfg, 'user')
                pwd = value_or_raise(cfg, 'password')
                backup_db(engine, db, user, pwd, output_path, compressor, aws_credential)
            else:
                raise ValueError('Invalid value for key type: %s' % backup_type)


def purge(purge_cfg, aws_credentials):
    pass


def send_slack_message(message, webhook=None, channel='#general', username='norris-backup', icon_emoji=':shipit:'):
    if webhook:
        requests.post(webhook, data=json.dumps({"text": message, "channel": channel, "username": username, "icon_emoji": icon_emoji}))


def run(config):
    aws_credentials = value_or_raise(config, 'aws_credentials')
    backup_cfg = config.get('backup', None)
    purge_cfg = config.get('purge', None)
    slack_cfg = config.get('notify', {}).get('slack', {})

    if backup_cfg:
        send_slack_message('Backup started.', **slack_cfg)
        backup(backup_cfg, aws_credentials)
        send_slack_message('Backup done.', **slack_cfg)

    if purge_cfg:
        send_slack_message('Purge started.', **slack_cfg)
        purge(purge_cfg, aws_credentials)
        send_slack_message('Purge done.', **slack_cfg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup your data to Amazon S3.', epilog='That\'s all folks.')
    parser.add_argument('--log', nargs='?', default='logging.yml', help='Log configuration file.')
    parser.add_argument('--config', nargs='?', default='norris.yml', help='Norris configuration file')
    args = parser.parse_args()

    with open(args.log, 'r') as f:
        logging.config.dictConfig(yaml.load(f))

    with open(args.config, 'r') as f:
        run(yaml.load(f))
