import json
import os
import time
from threading import Timer

import pandas as pd
import pika
from newsapi import NewsApiClient

from newsapi.newsapi_exception import NewsAPIException


class NewsPublisher:
    """
    A class to publish news articles to a RabbitMQ queue using the NewsAPI
    @param api_key: the api key to access the NewsAPI
    @param host: the host name of the RabbitMQ server
    @param queue_name: the name of the queue to publish the news articles
    """
    def __init__(self, api_key, host='localhost', queue_name='news_stream'):
        self.api = NewsApiClient(api_key=api_key)
        self.host = host
        self.queue_name = queue_name
        # set up a connection to RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.sources = 'bbc-news, cnn, fox-news, google-news, time, wired, the-new-york-times, the-wall-street-journal, the-washington-post, usa-today, abc-news, associated-press, bloomberg, business-insider, cbs-news, cnbc, entertainment-weekly, espn, fortune, fox-sports, mtv-news, national-geographic, nbc-news, new-scientist, newsweek, politico, reddit-r-all, reuters, the-hill, the-huffington-post, the-verge, the-washington-times, vice-news'

        try:
            self.articles = self.api.get_everything(sources=self.sources)
            self.headlines = self.api.get_top_headlines(sources=self.sources)
        except NewsAPIException as api_exception:
            print(f"Could not request results from NewsAPI; {api_exception}")
            print("Loading the news from the database...")

    def publish_news_data(self):
        """
        Publish the news articles to the RabbitMQ queue one by one and save the news to the database
        """
        try:
            self.publish_news_one_by_one()
        except NewsAPIException as api_exception:
            print(f"Could not request results from NewsAPI; {api_exception}")
            print("Loading the news from the database...")
            

        # do not close the connection until the message is delivered
        if self.connection.is_open:
            self.connection.close()

        # call the function again after 60 seconds
        Timer(60, self.publish_news_data).start()

    def publish_news_one_by_one(self):
        """
        Publish the news articles to the RabbitMQ queue one by one...
        """
        for _article in self.articles['articles']:
            _body = json.dumps(_article).encode('utf-8')
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=_body)
            print(f"Published a news article to the queue: {_article['title']}")
            # wait for 1 second before publishing the next article
            time.sleep(1)

        for _headline in self.headlines['articles']:
            _body = json.dumps(_headline).encode('utf-8')
            self.channel.basic_publish(exchange='', routing_key=f"{self.queue_name}_headlines", body=_body)
            print(f"Published a news headline to the queue: {_headline['title']}")
            # wait for 1 second before publishing the next article
            time.sleep(1)


def main():
    """
    The main function to run the server and publish the news articles to the RabbitMQ queue
    """
    print('Server is being initialized...')

    # get the api key from the environment variable
    api_key = os.environ.get('NEWSAPI_ORG')

    # create an instance of the NewsPublisher class
    api = NewsPublisher(api_key)

    # get the news from the newsapi
    api.publish_news_data()

    print('Server is now running...')


if __name__ == '__main__':
    main()
