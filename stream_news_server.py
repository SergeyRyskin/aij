import os
import re
from newsapi import NewsApiClient
import pika

# create a NewsApiClient object and set your API key
newsapi = NewsApiClient(api_key="898bee0f3753494d85afbb84f6268c0f")

# get the news dataset
news_data = []


# define a function to extract text from a news article
def get_headlines():
    # get the top headlines from BBC News
    top_headlines = newsapi.get_top_headlines(sources='bbc-news')
    # print the total number of news articles
    print(f'Total news articles: {top_headlines["totalResults"]}')
    return top_headlines['articles']


# preprocess the data
def preprocess(text):
    # remove all non-alphanumeric characters
    text = re.sub(r'\W+', ' ', text)

    # remove all digits
    text = re.sub(r'\d+', '', text)

    # remove all whitespace characters
    text = re.sub(r'\s+', ' ', text)

    # remove all leading and trailing whitespace characters
    text = text.strip()

    return text


for article in get_headlines():
    # extract the text from the news article
    text = article['title']

    # preprocess the text
    text = preprocess(text)

    # append the text to the news dataset
    news_data.append(text)


# publish the news dataset via RabbitMQ
def publish_news_data():
    # set up a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # declare a queue for the news data
    channel.queue_declare(queue='news_data')

    # publish each news article to the queue
    for text in news_data:
        channel.basic_publish(
            exchange='',
            routing_key='news_data',
            body=text.encode('utf-8'))

        print(f'Published news article: {text}')

    # do not close the connection until the message is delivered
    if connection.is_open:
        connection.close()


# call the publish_news_data function to publish the news dataset
publish_news_data()
