import boto3
import aws_util

class S3Bucket:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(bucket_name)

    def list_contents(self):
        print(f"\nContents of bucket {self.bucket_name}:")
        for obj in self.bucket.objects.all():
            print(obj.key)

    def upload_file(self, filename, key):
        try:
            self.bucket.upload_file(filename, key)
            print(f'Successfully uploaded {filename} to {self.bucket_name} with key {key}!')
        except Exception as e:
            print(f'Error uploading file: {e}')

    def download_file(self, key, filename):
        try:
            self.bucket.download_file(key, filename)
            print(f'Successfully downloaded {key} from {self.bucket_name} to {filename}!')
        except Exception as e:
            print(f'Error downloading file: {e}')

    def delete_file(self, key):
        try:
            self.bucket.Object(key).delete()
            print(f'Successfully deleted {key} from {self.bucket_name}!')
        except Exception as e:
            print(f'Error deleting file: {e}')


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
