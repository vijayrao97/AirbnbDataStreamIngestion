import json
import pandas as pd
import boto3
import io
import os
from datetime import date


def lambda_handler(event, context):
    # TODO implement
    print("Event : ", event)

    message = event[0]['message']
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    today_date = str(date.today())
    print(message)
    if (message == {}):
        return {}

    try:
        print("Enterying Try in")
        obj = s3_client.get_object(Bucket="airbnb-data-store-1307", Key=f"date={today_date}/Airbnb_{today_date}.csv")
        obj = obj['Body'].read()
        s = str(obj, 'utf-8')
        data = io.StringIO(s)
        df = pd.read_csv(data, index_col='bookingId')
        df.loc[message['bookingId']] = [message['userId'], message['porpertyId'], message['location'],
                                        message['startDate'], message['endDate'], message['price']]
        df.to_csv('/tmp/test.csv', encoding='utf-8')
        s3_resource.Bucket("airbnb-data-store-1307").upload_file("/tmp/test.csv",
                                                                 f"date={today_date}/Airbnb_{today_date}.csv")
        print(df)
    except Exception as e:
        print("Entering the exception")
        print(str(e))
        df = pd.DataFrame(columns=['bookingId', 'userId', 'porpertyId', 'location', 'startDate', 'endDate', 'price'])
        df = df.set_index(list(df.columns)[0])
        df.loc[message['bookingId']] = [message['userId'], message['porpertyId'], message['location'],
                                        message['startDate'], message['endDate'], message['price']]
        df.to_csv('/tmp/test.csv', encoding='utf-8')
        s3_resource.Bucket("airbnb-data-store-1307").upload_file("/tmp/test.csv",
                                                                 f"date={today_date}/Airbnb_{today_date}.csv")