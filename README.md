# Norris [![Build Status](https://travis-ci.org/alexandrevicenzi/norris-backup.svg?branch=master)](https://travis-ci.org/alexandrevicenzi/norris-backup)

Backup your files, folders and MySQL/MariaDB databases to Amazon S3.

## How to use

`python -m norris.norris --log=logging.yml --config=norris.yml`

## Compression

Backup type |no compress|zip|gzip|
------------|:---------:|:-:|:--:|
File        | ✔         | ✔ | ✘  |
Directory   | ✔         | ✔ | ✘  |
Database    | ✘         | ✔ | ✘  |

## Supported Databases

Databases  |Supported|
-----------|:-------:|
MySQL      | ✔       |
MariaDB    | ✔       |
PostgreSQL | ✘       |


## Get an access key

To get AWS access key see [AWS doc](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html).

## TODO

- Purge
- Directory upload without compress
- gzip support
- PostgreSQL support
