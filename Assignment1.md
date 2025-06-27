Assignment 1: Automated Instance Management Using AWS Lambda and Boto3

Objective:
Gain hands-on experience with AWS Lambda and Boto3, Amazon’s Python SDK and creation of a Lambda function that automatically starts or stops EC2 instances based on their tags.

Requirements:
1. Setup EC2 Instances
2. Create IAM Role for Lambda
3. Write and Deploy Lambda Function
4. Test and Verify

⚙️ Step-by-Step Instructions

1. EC2 Setup
Go to the EC2 Dashboard in AWS Console.

Launch two EC2 instances and Tag the instances:
First instance: Key = Action | Value = Auto-Stop
Second instance: Key = Action | Value = Auto-Start
![image](https://github.com/user-attachments/assets/36696a9a-c4db-4419-a30a-a25782789ffc)


2. Create IAM Role for Lambda
Go to the IAM Dashboard:
Create a new IAM role with trusted entity Lambda.
Attach the policy AmazonEC2FullAccess to this role.
![image](https://github.com/user-attachments/assets/8f5a0cf2-bb0a-4683-bb8c-f2111dbf2287)

3. Create Lambda Function
Open the AWS Lambda Dashboard:
Click Create function.
Choose Python 3.13 runtime.
Attach the IAM role you created.
![image](https://github.com/user-attachments/assets/f4e64430-1357-43f3-b8e0-7689e85f7313)

Write the following Python script on Lambda code:

import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Stop instances with Action=Auto-Stop tag
    stop_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    stop_ids = []
    for reservation in stop_instances['Reservations']:
        for instance in reservation['Instances']:
            stop_ids.append(instance['InstanceId'])

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Stopped instances: {stop_ids}")
    else:
        print("No instances to stop.")

    # Start instances with Action=Auto-Start tag
    start_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )

    start_ids = []
    for reservation in start_instances['Reservations']:
        for instance in reservation['Instances']:
            start_ids.append(instance['InstanceId'])

    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Started instances: {start_ids}")
    else:
        print("No instances to start.")

This script:
Finds all running instances tagged Auto-Stop and stops them.
Finds all stopped instances tagged Auto-Start and starts them.

Prints the instance IDs for logging.

4. Test the Lambda Function
   
Deploy your Lambda function.
Click Test and run it manually.

Go back to the EC2 Dashboard to verify:
The Auto-Stop instance is stopped.
The Auto-Start instance is running.

Instances before runing the script:
![image](https://github.com/user-attachments/assets/0918edd4-81bf-4840-97c9-d6d79e414152)

Instances after runing the script:
![image](https://github.com/user-attachments/assets/5327ace1-c73c-4e68-8d77-22805b4372d8)
![image](https://github.com/user-attachments/assets/6802c8b1-840e-43cc-a4bc-18121c619593)

Execution Succeeded:
![image](https://github.com/user-attachments/assets/a4f7000e-e205-42fa-ab59-037fa818a291)
