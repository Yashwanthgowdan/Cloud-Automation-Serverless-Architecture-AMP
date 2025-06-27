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

![image](https://github.com/user-attachments/assets/5d497e26-e576-4507-9ef7-b9a4be114a32)


2️. Create Lambda IAM Role
Open the IAM Dashboard.
Create a new role for Lambda.
Attach the AmazonS3FullAccess policy.

![image](https://github.com/user-attachments/assets/983ae9d7-5c3d-4b95-a4a6-f1f05ed7b7c2)

3️. Create Lambda Function
Open the AWS Lambda Dashboard.
Click Create Function.
Choose Python 3.13 runtime.
Attach the IAM role you created above.

![image](https://github.com/user-attachments/assets/1326e8c6-65cd-4214-a9a2-0a83736e0ac4)

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
Output: (There are no 30 days older files)

![image](https://github.com/user-attachments/assets/fd71b857-9cb7-4473-b98c-517028772fd7)
 
 Modified the code to 10 minutes older files on line number 16:
 Before executing the function:
 
 ![image](https://github.com/user-attachments/assets/ffd2fa39-ae42-4568-b5fb-14265f8b2566)
Execution succeeded:

![image](https://github.com/user-attachments/assets/ee7b1379-b9e5-4423-8a07-357f1254dea6)
After Script execution:

![image](https://github.com/user-attachments/assets/9b3a4ba0-94db-424d-afd7-806818ac1d24)
