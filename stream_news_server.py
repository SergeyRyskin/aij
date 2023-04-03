import json
import os
import time
from threading import Timer

import pandas as pd
import pika
from newsapi import NewsApiClient

import motor.motor_asyncio
from newsapi.newsapi_exception import NewsAPIException


class NewsPublisher:
    def __init__(self, api_key, host='localhost', queue_name='news_stream'):
        self.api = NewsApiClient(api_key=api_key)
        self.host = host
        self.queue_name = queue_name
        # set up a connection to RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.sources = 'bbc-news, cnn, fox-news, google-news, the-new-york-times, the-wall-street-journal, the-washington-post, time, usa-today, wired'

        try:
            self.articles = self.api.get_everything(sources=self.sources)
            self.headlines = self.api.get_top_headlines(sources=self.sources)
        except NewsAPIException as e:
            print(f"Could not request results from NewsAPI; {e}")
            print("Loading the news from the database...")
            self.get_news_from_mongodb()

    def publish_news_data(self):
        # publish all the news sources
        try:
            self.publish_news_one_by_one()
        except NewsAPIException as e:
            print(f"Could not request results from NewsAPI; {e}")
            print("Loading the news from the database...")
            self.get_news_from_mongodb()

        # do not close the connection until the message is delivered
        if self.connection.is_open:
            self.connection.close()

        # call the function again after 60 seconds
        Timer(60, self.publish_news_data).start()

    def publish_news_one_by_one(self):

        for article in self.articles['articles']:
            self.channel.basic_publish(exchange='', routing_key=self.queue_name,
                                       body=json.dumps(article).encode('utf-8'))

    def save_news_to_mongodb(self):

        # create a mongodb document for each news article

        # create a dataframe
        df = pd.DataFrame(self.articles['articles'])

        for i, row in df.iterrows():
            df.at[i, 'title'] = row['title'].replace('\n', ' ')

        # drop duplicates
        df.drop_duplicates(inplace=True)

        # save the news to the database
        motor_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

        db = motor_client['news']

        collection = db['news_google-news']

        collection.insert_many(df.to_dict('records'))

        return df

    def get_news_from_mongodb(self):
        motor_client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
        db = motor_client['news']
        collection = db['news_google-news']
        cursor = collection.find()

        for document in cursor:
            self.articles['articles'].append(document['title'])


def main():
    # print that the server is running
    print('Server is running...')

    # get the api key from the environment variable
    api_key = os.environ.get('NEWSAPI_ORG')

    # create an instance of the NewsPublisher class
    api = NewsPublisher(api_key)

    # get the news from the newsapi
    api.publish_news_data()

    print('Server is stopped...')


if __name__ == '__main__':
    main()
