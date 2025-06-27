Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

Objective:
Gain practical experience with AWS Lambda and Boto3 by creating a Lambda function that automatically deletes files older than 30 days in an S3 bucket.

Task Goal: Automate the cleanup of old files in S3.

What this task does:
Lists objects in the bucket.
Checks their last modified date.
Deletes files older than 30 days.
Logs which files were deleted.

Step-by-Step Instructions
1. S3 Bucket Setup:
Go to the S3 Dashboard.
Create a new bucket.
Upload multiple test files(old files if can)

2️. Create Lambda IAM Role
Open the IAM Dashboard.
Create a new role for Lambda.
Attach the AmazonS3FullAccess policy.

3️. Create Lambda Function
Open the AWS Lambda Dashboard.
Click Create Function.
Choose Python 3.13 runtime.
Attach the IAM role you created above.

Add the following Python script:

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

How it works
Initialize the S3 client.
List objects using list_objects_v2.
Compare LastModified with today’s date minus 30 days.
Delete matching files.
Print which files were removed.

4️. Manual Invocation
Save and deploy your Lambda function.
Create a test event.
Click Test to run.

Go back to the S3 dashboard — confirm:
Files older than 30 days are gone.
Newer files remain.
