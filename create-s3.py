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


# Set the name of your bucket and the domain name you want to use
bucket_name = 'apatruno-photos'
domain_name = 'photo.apatruno.com'

# Check if the S3 bucket already exists
try:
    s3.head_bucket(Bucket=bucket_name)
    print(f"S3 bucket '{bucket_name}' already exists")
except:
    # Create the S3 bucket if it doesn't exist
    s3.create_bucket(Bucket=bucket_name)
    print(f"Created S3 bucket '{bucket_name}'")

# Configure the bucket for static website hosting
s3.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'}
    }
)
print(f"Configured S3 bucket '{bucket_name}' for static website hosting")

# Set the bucket policy to allow public read access
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }
    ]
}
s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
print(f"Set bucket policy for S3 bucket '{bucket_name}' to allow public read access")

# Create a new Route 53 DNS record to map your subdomain to the S3 bucket URL
route53 = boto3.client('route53',aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)
hosted_zones = route53.list_hosted_zones_by_name(DNSName=domain_name)

if hosted_zones['HostedZones']:
    zone_id = hosted_zones['HostedZones'][0]['Id']
    record_name = f"{domain_name}."
    record_type = 'CNAME'
    record_ttl = 300
    record_value = f"{bucket_name}.s3-website-us-east-1.amazonaws.com"

    # Check if the DNS record already exists
    existing_records = route53.list_resource_record_sets(HostedZoneId=zone_id, StartRecordName=record_name, StartRecordType=record_type)['ResourceRecordSets']
    if len(existing_records) > 0 and existing_records[0]['Name'] == record_name and existing_records[0]['Type'] == record_type and existing_records[0]['ResourceRecords'][0]['Value'] == record_value:
        print(f"DNS record '{record_name}' already exists with the correct configuration")
    else:
        # Create the DNS record if it doesn't exist
        apex_domain_name = 'apatruno.com'

        route53.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': apex_domain_name,
                        'Type': record_type,
                        'TTL': record_ttl,
                        'ResourceRecords': [{
                            'Value': record_value
                        }]
                    }
                }]
            }
        )
        print(f"Created DNS record '{record_name}' to map to S3 bucket '{bucket_name}'")
else:
    print(f"Hosted zone for domain '{domain_name}' not found")
    

print(f"Your website is now available at: http://{domain_name}")