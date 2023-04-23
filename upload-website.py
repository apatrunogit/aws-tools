import configparser
import boto3
import json
import time

# Read AWS credentials from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
aws_access_key_id = config['default']['aws_access_key_id']
aws_secret_access_key = config['default']['aws_secret_access_key']

# Create S3 client using AWS credentials
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# list all S3 buckets
response = s3.list_buckets()

# print a numbered list of bucket names
print('Available S3 Buckets:')
for i, bucket in enumerate(response['Buckets'], start=1):
    print(f"{i}. {bucket['Name']}")

# ask user to select a bucket by number or name
bucket_choice = input('Enter the number or name of the bucket to upload the index.html file to: ')
if bucket_choice.isdigit() and int(bucket_choice) <= len(response['Buckets']):
    bucket_name = response['Buckets'][int(bucket_choice) - 1]['Name']
else:
    bucket_name = bucket_choice

# upload the index.html file to the selected bucket
try:
    s3.upload_file('index.html', bucket_name, 'index.html')
    print(f'Successfully uploaded index.html to {bucket_name}!')
except Exception as e:
    print(f'Error uploading file: {e}')
