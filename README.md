# Backup your data to Amazon S3

Backup your files, folders and MySQL/MariaDB databases to Amazon S3.

This is a useful tool to backup your Wordpress site.

## Requirements

- Python 2.7+
- Boto 2.3+
- Yaml

## Usage

The best option is to schedule this script to run everyday.

#### Backup a folder

```bash
python backup.py --dir /path/to/my/folder --bucket mybucket --aws_access_key_id YOUR_ID --aws_secret_access_key YOUR_KEY
```

#### Backup a file

```bash
python backup.py --dir /path/to/my/file.txt --bucket mybucket --aws_access_key_id YOUR_ID --aws_secret_access_key YOUR_KEY
```
#### Backup a database

```bash
python backup.py --db my_database --user root --pwd my_pwd --bucket mybucket --aws_access_key_id YOUR_ID --aws_secret_access_key YOUR_KEY
```
You can set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY as environment variables if you want. See [Boto doc](http://boto.readthedocs.org/en/latest/s3_tut.html).

## Logging

Setup `logging.yml` as you want. There's a simple example for console and file logging.

## Get an access key

To get AWS access key see [AWS doc](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html).

## TODO

- Yml file as an input for norris, instead command line arguments.
- Upload old files, if there's an crash and zip file still available to upload.
