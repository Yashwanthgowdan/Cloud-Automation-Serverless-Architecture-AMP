import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'YOUR_BUCKET_NAME'  # Replace with your bucket name

    # Get the list of all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in response:
        print("No objects found in the bucket.")
        return

    # Calculate the threshold date
    threshold_date = datetime.now(timezone.utc) - timedelta(days=30)

    deleted_files = []

    for obj in response['Contents']:
        key = obj['Key']
        last_modified = obj['LastModified']

        if last_modified < threshold_date:
            # Delete the object
            s3.delete_object(Bucket=bucket_name, Key=key)
            deleted_files.append(key)

    if deleted_files:
        print(f"Deleted objects older than 30 days: {deleted_files}")
    else:
        print("No objects older than 30 days found.")