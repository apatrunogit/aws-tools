import boto3
import time
import configparser

# Read AWS credentials from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
aws_access_key_id = config['default']['aws_access_key_id']
aws_secret_access_key = config['default']['aws_secret_access_key']

def create_hosted_zone(domain_name):
    """
    Create a new Route 53 hosted zone for the specified domain.
    Returns the hosted zone ID if successful, None otherwise.
    """
    route53 = boto3.client(
        'route53',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    response = route53.create_hosted_zone(
        Name=domain_name,
        CallerReference=str(time.time())
    )
    return response.get('HostedZone', {}).get('Id')

def check_hosted_zone(domain_name):
    """
    Check if a hosted zone exists for the specified domain.
    Returns the hosted zone ID if found, None otherwise.
    """
    route53 = boto3.client(
        'route53',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    response = route53.list_hosted_zones_by_name(DNSName=domain_name)
    if response['HostedZones']:
        return response['HostedZones'][0]['Id']
    return None

# Replace with your domain name
domain_name = 'photo.apatruno.com'

# Check if a hosted zone already exists for the domain
hosted_zone_id = check_hosted_zone(domain_name)

if hosted_zone_id:
    print(f"Hosted zone '{domain_name}' already exists with ID '{hosted_zone_id}'")
else:
    # Create a new hosted zone for the domain
    hosted_zone_id = create_hosted_zone(domain_name)
    if hosted_zone_id:
        print(f"Created hosted zone '{domain_name}' with ID '{hosted_zone_id}'")
    else:
        print(f"Failed to create hosted zone for domain '{domain_name}'")
