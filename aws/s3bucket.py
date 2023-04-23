import boto3
import aws_util

class S3Bucket:
    def __init__(self, session: boto3.Session, bucket_name: str):
        self.s3 = session.client('s3')
        self.bucket_name = bucket_name

    def list_contents(self) -> List[str]:
        response = self.s3.list_objects(Bucket=self.bucket_name)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        else:
            return []

    def upload_file(self, filename: str, key: str) -> bool:
        try:
            self.s3.upload_file(filename, self.bucket_name, key)
            return True
        except Exception as e:
            print(f'Error uploading file: {e}')
            return False

    def download_file(self, key: str, filename: str) -> bool:
        try:
            self.s3.download_file(self.bucket_name, key, filename)
            return True
        except Exception as e:
            print(f'Error downloading file: {e}')
            return False

    def delete_file(self, key: str) -> bool:
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except Exception as e:
            print(f'Error deleting file: {e}')
            return False



def main():
    # Create S3 client
    session = aws_util.get_aws_session
    s3 = session.client('s3')

    # List all S3 buckets
    response = s3.list_buckets()

    # Print a numbered list of bucket names
    print('Available S3 Buckets:')
    for i, bucket in enumerate(response['Buckets'], start=1):
        print(f"{i}. {bucket['Name']}")

    # Ask user to select a bucket by number or name
    bucket_choice = input('Enter the number or name of the bucket: ')
    if bucket_choice.isdigit() and int(bucket_choice) <= len(response['Buckets']):
        bucket_name = response['Buckets'][int(bucket_choice) - 1]['Name']
    else:
        bucket_name = bucket_choice

    # Initialize S3Bucket object
    bucket = S3Bucket(bucket_name)

    # Actions menu
    while True:
        print(f"\nSelected bucket: {bucket_name}\n")
        print("Choose an action:")
        print("1. List bucket contents")
        print("2. Upload file to bucket")
        print("3. Download file from bucket")
        print("4. Delete file from bucket")
        print("5. Quit")

        action_choice = input('Enter action number: ')

        if action_choice == '1':
            # List bucket contents
            bucket.list_contents()

        elif action_choice == '2':
            # Upload file to bucket
            filename = input('Enter filename to upload: ')
            key = input('Enter key name for file in bucket: ')
            bucket.upload_file(filename, key)

        elif action_choice == '3':
            # Download file from bucket
            key = input('Enter key name for file in bucket: ')
            filename = input('Enter filename to save to: ')
            bucket.download_file(key, filename)

        elif action_choice == '4':
            # Delete file from bucket
            key = input('Enter key name for file in bucket: ')
            bucket.delete_file(key)

        elif action_choice == '5':
            # Quit
            print('Exiting...')
            break

        else:
            print('Invalid choice. Please choose a valid action.')


if __name__ == '__main__':
    main()
