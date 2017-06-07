import tweepy
import os

consumer_key = os.environ.get('TW_CONSUMER_KEY')
consumer_secret = os.environ.get('TW_CONSUMER_SECRET')
access_token = os.environ.get('TW_ACCESS_TOKEN')
access_token_secret = os.environ.get('TW_ACCESS_TOKEN_SECRET')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def print_followers():
    for follower in tweepy.Cursor(api.followers).items():
        print "Name: %s. Location: %s" % (follower.name, follower.location)
        follower.follow()
        print "================"

def print_user(user_id):
    user = api.get_user(user_id)
    print user.screen_name
    print user.followers_count
    for friend in user.friends():
       print friend.screen_name


def print_timeline():
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print "----------------------"
        print tweet.text


# print_timeline()
# print_followers()
print_user('botsplash_')
