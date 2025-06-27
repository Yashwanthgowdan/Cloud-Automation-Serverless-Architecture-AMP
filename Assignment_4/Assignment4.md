Assignment 8: Analyze Sentiment of User Reviews Using AWS Lambda, Boto3, and Amazon Comprehend

Objective:
Learn how to use Amazon Comprehend with AWS Lambda to automatically analyze the sentiment of text — such as user reviews — and log whether the sentiment is Positive, Negative, Neutral, or Mixed.

Task Goal: 
Analyze the sentiment of text using Amazon Comprehend.

What it does:
Takes text input.
Calls Comprehend’s detect_sentiment API.
Logs the result.

Step-by-Step Instructions
1️. Create Lambda IAM Role
Open the IAM Dashboard.
Create a new IAM role for Lambda.
Attach the AmazonComprehendFullAccess policy.
![image](https://github.com/user-attachments/assets/0215467d-0991-441a-a763-5a004bdd5772)

2️. Create Lambda Function
Open the AWS Lambda Dashboard.
Click Create Function.
Choose Python 3.13 runtime.
Attach the IAM role created above.
![image](https://github.com/user-attachments/assets/7e75fc47-ac2d-4652-a472-c67d8ee4d3d4)

Add the following Python script:

import boto3

def lambda_handler(event, context):
    # Initialize Comprehend client
    comprehend = boto3.client('comprehend')

    # Get the text to analyze from the event
    text = event.get('review', '')
    if not text:
        print("No review text provided in the event.")
        return

    # Call Amazon Comprehend to detect sentiment
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'  # Use 'en' for English reviews
    )

    sentiment = response['Sentiment']
    sentiment_score = response['SentimentScore']

    print(f"Review text: {text}")
    print(f"Detected sentiment: {sentiment}")
    print(f"Sentiment scores: {sentiment_score}")

    return {
        'Sentiment': sentiment,
        'SentimentScore': sentiment_score
    }

How It Works
Input - Takes a review string from the event payload.
Detect - Calls detect_sentiment using Boto3.
Output - Logs and returns the sentiment label + confidence scores.

3️. Testing
Save and deploy the function.
Create a test event in Lambda with JSON input, for example:
{
  "review": "I absolutely love this product! It works great and the support team is amazing."
}
Click Test.
![image](https://github.com/user-attachments/assets/a64025b7-8e3d-4f20-b5b7-643f27d9e46e)

View the Lambda logs in CloudWatch to see:
The input text.
The detected sentiment (e.g., Positive).
The detailed sentiment scores.
