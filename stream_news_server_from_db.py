import json
from threading import Timer
import pandas as pd
import pika


class NewsPublisher:
    def __init__(self, host='localhost', queue_name='news_stream', dataframe='news/articles.csv'):
        self.host = host
        self.queue_name = queue_name
        # set up a connection to RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.sources = 'bbc-news, cnn, fox-news, google-news, the-new-york-times, the-wall-street-journal, the-washington-post, time, usa-today, wired'

        # declare the queue
        self.channel.queue_declare(queue=self.queue_name)
        self.articles = pd.read_csv(dataframe)

        # remove the rows with empty title and duplicate title
        self.articles = self.articles.dropna(subset=['title'])
        self.articles = self.articles.drop_duplicates(subset=['title'])

        # remove the rows with empty description and duplicate description
        self.articles = self.articles.dropna(subset=['description'])
        self.articles = self.articles.drop_duplicates(subset=['description'])

        # add another column to mark the news as published
        self.articles['published'] = False

        # get the latest row to publish, but first sort by published date
        self.articles = self.articles.sort_values(by=['publishedAt'], ascending=False)
        self.next_row = self.articles[False == self.articles['published']].head(1)

    def publish(self):
        # publish the news to the queue
        if self.next_row is not None:
            # get the news
            news = self.next_row.to_dict('records')[0]

            # mark the news as published
            self.articles.loc[self.articles['title'] == news['title'], 'published'] = True

            # get the next news to publish
            self.next_row = self.articles[False == self.articles['published']].head(1)

            # publish the news to the queue
            self.channel.basic_publish(exchange='',
                                       routing_key=self.queue_name,
                                       body=json.dumps(news).encode('utf-8'))

            print('Published: {}'.format(news['title']))

    def publish_continuously(self, interval=1):
        # publish the news to the queue continuously
        self.publish()
        Timer(interval, self.publish_continuously, [interval]).start()

    def close(self):
        # close the connection
        if self.connection:
            self.connection.close()


def main():
    # print that the server is running
    print('Server is running...')

    # create a news publisher
    news_publisher = NewsPublisher()

    # publish the news
    news_publisher.publish_continuously()

    print('Server is stopped...')


if __name__ == '__main__':
    main()
