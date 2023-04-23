import configparser
import boto3

# Read AWS credentials from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
aws_access_key_id = config['default']['aws_access_key_id']
aws_secret_access_key = config['default']['aws_secret_access_key']

# Create Route53 client using AWS credentials
route53 = boto3.client(
    'route53',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Set the name of your domain
domain_name = 'photo.apatruno.com'

# Check if the hosted zone for the domain already exists
hosted_zones = route53.list_hosted_zones_by_name(DNSName=domain_name)
if hosted_zones['HostedZones']:
    zone_id = hosted_zones['HostedZones'][0]['Id']
    print(f"Hosted zone for domain '{domain_name}' found with ID '{zone_id}'")
else:
    # Create the hosted zone if it doesn't exist
    response = route53.create_hosted_zone(Name=domain_name, CallerReference=str(time.time()))
    zone_id = response['HostedZone']['Id']
    print(f"Created hosted zone for domain '{domain_name}' with ID '{zone_id}'")