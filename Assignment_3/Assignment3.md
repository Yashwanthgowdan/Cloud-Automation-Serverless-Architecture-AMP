Assignment 3: Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3
✅ Objective
Improve your AWS security posture by creating an AWS Lambda function that automatically detects S3 buckets without server-side encryption (SSE).

📌 Task Overview
Goal: Find S3 buckets that do not have server-side encryption enabled.

What it does:

Lists all buckets in your account.

Checks their encryption configuration.

Logs bucket names that are unencrypted.

⚙️ Step-by-Step Instructions
1️⃣ S3 Bucket Setup
Open the S3 Dashboard.

Create multiple S3 buckets:

Make sure some have server-side encryption enabled (AES-256 or aws:kms).

Leave some unencrypted to test detection.

2️⃣ Create Lambda IAM Role
Open the IAM Dashboard.

Create a new IAM role for Lambda.

Attach the AmazonS3ReadOnlyAccess policy.
✅ This is sufficient since you’re only reading configuration, not modifying buckets.

3️⃣ Create Lambda Function
Open the AWS Lambda Dashboard.

Click Create Function.

Choose Python 3.x runtime.

Attach the IAM role created in step 2.

Copy and paste the following Python script:

🐍 Example Lambda Python Script
python
Copy
Edit
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
✅ How it works
Step	Details
1️⃣	Uses list_buckets to find all buckets.
2️⃣	Calls get_bucket_encryption for each bucket.
3️⃣	If ServerSideEncryptionConfigurationNotFoundError is raised, the bucket is unencrypted.
4️⃣	Prints out the names of all unencrypted buckets.

4️⃣ Manual Invocation
Deploy your Lambda function.

Create a test event (an empty JSON {} works fine).

Click Test.

Check the Lambda logs in CloudWatch.

You’ll see which buckets are unencrypted.

