# Wordpress backup to Amazon S3

Backup your files, folders and MySQL/MariaDB databases to Amazon S3.

This is a useful tool to backup your Wordpress site.

## Requirements

- Python 2.7+
- Boto 2.3+

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