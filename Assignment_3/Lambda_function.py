import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Get the list of all buckets
    response = s3.list_buckets()
    buckets = response['Buckets']

    unencrypted_buckets = []

    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            enc = s3.get_bucket_encryption(Bucket=bucket_name)
            rules = enc['ServerSideEncryptionConfiguration']['Rules']
            print(f"Bucket '{bucket_name}' is encrypted with rules: {rules}")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                # This means the bucket does not have server-side encryption enabled
                unencrypted_buckets.append(bucket_name)
            else:
                print(f"Error checking encryption for bucket {bucket_name}: {e}")

    if unencrypted_buckets:
        print(f"Buckets WITHOUT server-side encryption: {unencrypted_buckets}")
    else:
        print("All buckets have server-side encryption enabled.")
