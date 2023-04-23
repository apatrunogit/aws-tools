import boto3
import configparser

def create_session(profile_name='default', region_name='us-west-2'):
    config = configparser.ConfigParser()
    config.read('config.ini')

    access_key = config.get(profile_name, 'aws_access_key_id')
    secret_key = config.get(profile_name, 'aws_secret_access_key')

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name
    )

    return session
