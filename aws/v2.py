import boto3
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Create a Route53 client
route53 = boto3.client('route53',
                       aws_access_key_id=config['default']['aws_access_key_id'],
                       aws_secret_access_key=config['default']['aws_secret_access_key'])

# Check if the hosted zone exists
zone_name = 'photo.apatruno.com.'
existing_zones = route53.list_hosted_zones_by_name(DNSName=zone_name)['HostedZones']
if not existing_zones:
    print(f"The hosted zone {zone_name} does not exist. Aborting.")
    exit(1)
zone_id = existing_zones[0]['Id']

# Check if the record already exists
record_name = 'apatruno.com.'
existing_records = route53.list_resource_record_sets(HostedZoneId=zone_id, StartRecordName=record_name)['ResourceRecordSets']
if any(record['Name'] == f"{record_name}." for record in existing_records):
    print(f"The record {record_name} already exists. Aborting.")
    exit(1)

# Create a new record set
change_batch = {
    'Comment': 'Create a record set for the website',
    'Changes': [
        {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': f'{record_name}.',
                'Type': 'A',
                'AliasTarget': {
                    'HostedZoneId': 'Z21DNDUVLTQW6Q',
                    'DNSName': 's3-website-us-east-1.amazonaws.com.',
                    'EvaluateTargetHealth': False
                }
            }
        }
    ]
}
route53.change_resource_record_sets(HostedZoneId=zone_id, ChangeBatch=change_batch)

print(f"The record {record_name} has been successfully created!")
