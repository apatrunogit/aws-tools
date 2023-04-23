import configparser
import boto3

def get_aws_session():
    # Read AWS credentials from config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    aws_access_key_id = config['default']['aws_access_key_id']
    aws_secret_access_key = config['default']['aws_secret_access_key']
    # Create boto3 session object with the credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    return session


def update_content_type(bucket_name):
    session = get_aws_session()
    s3 = session.client('s3')

    # Check if index.html file exists in the bucket
    try:
        s3.head_object(Bucket=bucket_name, Key='index.html')
    except s3.exceptions.NoSuchKey:
        print('index.html does not exist in the bucket')
        return

    # Check content type of index.html file
    response = s3.head_object(Bucket=bucket_name, Key='index.html')
    content_type = response['ContentType']

    # If content type is not text/html, update it
    if content_type != 'text/html':
        s3.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': 'index.html'}, Key='index.html', ContentType='text/html')
        print('Content type of index.html updated to text/html')
    else:
        print('Content type of index.html is already text/html')
