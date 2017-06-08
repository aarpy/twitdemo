import os
import tweepy

from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from google.cloud import language

TWITTER_CONSUMER_KEY = os.environ.get('TW_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TW_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TW_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TW_ACCESS_TOKEN_SECRET')

API_RETRY_COUNT = 60
API_RETRY_DELAY_S = 1
API_RETRY_ERRORS = [400, 401, 500, 502, 503, 504]


gcnl_client = language.Client()

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        print "---------------------"
        print "Screen name: %s" % (tweet.author.screen_name)
        print "Text: %s" % (tweet.text)
        if not tweet.text:
            return

        document = gcnl_client.document_from_text(tweet.text)
        sentiment = document.analyze_sentiment()
        print "Sentiment score: %s;%s." % (sentiment.score, sentiment.magnitude)

        entities = document.analyze_entities()
        for entity in entities:
            mentions = ", ".join(['"%s"' % mention for mention in entity.mentions])
            print("entity: %s; %s" % (entity.name, entity.entity_type))
            print("   mentions: %s" % (mentions))

    def on_error(self, status_code):
        print "================="
        print "stream error: %d" % (status_code)


twitter_auth = OAuthHandler(TWITTER_CONSUMER_KEY,
                            TWITTER_CONSUMER_SECRET)
twitter_auth.set_access_token(TWITTER_ACCESS_TOKEN,
                              TWITTER_ACCESS_TOKEN_SECRET)

twitter_api = API(auth_handler=twitter_auth,
                  retry_count=API_RETRY_COUNT,
                  retry_delay=API_RETRY_DELAY_S,
                  retry_errors=API_RETRY_ERRORS,
                  wait_on_rate_limit=True,
                  wait_on_rate_limit_notify=True)

twitter_listener = MyStreamListener()
twitter_stream = Stream(twitter_auth, twitter_listener)
twitter_stream.filter(track=['python'])
# twitter_stream.filter(follow=['48600916'])
