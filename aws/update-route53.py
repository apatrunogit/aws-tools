import boto3
import configparser
import json
import time 

# Read AWS credentials from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
aws_access_key_id = config['default']['aws_access_key_id']
aws_secret_access_key = config['default']['aws_secret_access_key']

# Create Route53 client using AWS credentials
route53 = boto3.client('route53', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Set the domain name and subdomain you want to use
domain_name = 'apatruno.com'
subdomain_name = 'photo'

# Create a new hosted zone for your domain if it doesn't already exist
try:
    route53.create_hosted_zone(
        Name=domain_name,
        CallerReference=str(time.time())
    )
    print(f"Created hosted zone for domain '{domain_name}'")
except route53.exceptions.AlreadyExistsException:
    print(f"Hosted zone for domain '{domain_name}' already exists")

# Get the ID of the hosted zone for your domain
response = route53.list_hosted_zones_by_name(DNSName=domain_name)
if response['HostedZones']:
    zone_id = response['HostedZones'][0]['Id']
    print(f"Found hosted zone ID '{zone_id}' for domain '{domain_name}'")
else:
    print(f"No hosted zones found for domain '{domain_name}'")
    exit()

# Create a new CNAME record to map your subdomain to the S3 bucket URL
bucket_name = 'apatruno-photos'
s3_website_endpoint = f"{bucket_name}.s3-website-us-east-1.amazonaws.com"
record_name = f"{subdomain_name}.{domain_name}"
record_type = 'CNAME'
record_ttl = 300

change_batch = {
    'Changes': [{
        'Action': 'UPSERT',
        'ResourceRecordSet': {
            'Name': record_name,
            'Type': record_type,
            'TTL': record_ttl,
            'ResourceRecords': [{
                'Value': s3_website_endpoint
            }]
        }
    }]
}

response = route53.change_resource_record_sets(
    HostedZoneId=zone_id,
    ChangeBatch=change_batch
)

print(f"Created CNAME record '{record_name}' to map to S3 bucket '{bucket_name}'")
