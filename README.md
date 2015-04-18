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
python norris.py --dir /path/to/my/folder --bucket mybucket --aws_access_key_id YOUR_ID --aws_secret_access_key YOUR_KEY
```

#### Backup a file

```bash
python norris.py --dir /path/to/my/file.txt --bucket mybucket --aws_access_key_id YOUR_ID --aws_secret_access_key YOUR_KEY
```
#### Backup a database

```bash
python norris.py --db my_database --user root --pwd my_pwd --bucket mybucket --aws_access_key_id YOUR_ID --aws_secret_access_key YOUR_KEY
```
Run `python norris.py` to see all command line options.

You can set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY as environment variables if you want. You can see more on [boto doc](http://boto.readthedocs.org/en/latest/s3_tut.html).

## Logging

Setup `logging.yml` as you want. There's a simple example for console and file logging.

If you want to be mailed when an error occurred try `logging-with_email.yml`.

## Get an access key

To get AWS access key see [AWS doc](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html).

## Upload

To upload a file to S3 bucket, you need to create it manually with AWS Console. Norris, as boto, doesn't do this for you.

All files uploaded to S3 are zipped (Deflate).

## TODO

- Yaml file as an input for norris, instead command line arguments.
- Upload old files, if there's an crash and zip file still available to upload.
