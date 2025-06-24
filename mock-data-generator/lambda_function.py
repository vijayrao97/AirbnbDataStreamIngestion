import json
import boto3
import random
import string
from datetime import datetime, timedelta

sqs_client = boto3.client('sqs')
QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/247019597173/AirbnbBookingQueue'


def generate_sales_order():
    countryList = ["Mumbai, India", "Bengaluru, India", "Hyderabad, India", "Chennai, India", "Delhi, India"]

    min_date = datetime(2023, 1, 1)
    max_date = datetime(2023, 1, 31)

    # Generate random start_date
    start_date = min_date + timedelta(days=random.randint(0, (max_date - min_date).days - 1))

    # Generate random end_date after the start_date
    end_date = start_date + timedelta(days=random.randint(1, (max_date - start_date).days))

    return {
        "bookingId": random.randint(10000, 99999),
        "userId": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        "porpertyId": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        "location": random.choice(countryList),
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "price": '$ ' + str(random.randint(100, 999))
    }


def lambda_handler(event, context):
    # TODO implement
    i = 0
    while (i < 20):
        sales_order = generate_sales_order()
        print(sales_order)
        sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(sales_order)
        )
        i = i + 1

    return {
        'statusCode': 200,
        'body': json.dumps('AirBnB data published to SQS!')
    }