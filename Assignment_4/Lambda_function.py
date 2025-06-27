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
