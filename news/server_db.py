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

        # declare the queue for articles to be published
        self.channel.queue_declare(queue=self.queue_name)
        self.articles = pd.read_csv(dataframe)

        # declare the queue for titles to be published
        self.channel.queue_declare(queue='news_titles')

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

        # convert all article titles to one string
        self.titles = self.articles['title'].str.cat(sep=' ... | ')

    def publish(self):
        # publish the news to the queue
        if self.next_row is not None:
            # get the news
            # if still have news to publish
            if self.next_row.shape[0] > 0:
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

            else:
                # if no more news to publish, then reset the published column
                self.articles['published'] = False
                self.next_row = self.articles[False == self.articles['published']].head(1)
                print('No more news to publish. Reset the published column to False.')

    def publish_continuously(self, interval=1):
        # publish the news to the queue continuously
        self.publish()
        Timer(interval, self.publish_continuously, [interval]).start()

    def publish_titles(self):
        # publish the news to the queue
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=self.titles.encode('utf-8'))

    def publish_titles_continuously(self, interval=60):
        # publish the news to the queue continuously
        self.publish_titles()
        Timer(interval, self.publish_titles_continuously, [interval]).start()

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

    # publish the news titles
    news_publisher.publish_titles()


if __name__ == '__main__':
    main()
