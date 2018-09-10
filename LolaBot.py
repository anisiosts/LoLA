from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
import TwitterCredentials as tc
from LolaOrganizer import LolaOrganizer

# # # TWITTER CLIENT # # #

# # # TWITTER AUTHENTICATOR # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(tc.CONSUMER_KEY, tc.CONSUMER_SECRET)
        auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
        return auth

# # # TWITTER STREAMER # # #
class TwitterStreamer():
    # A class for streaming and processing live tweets.
    
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, tweets_filename, hash_tag_list):
        # This handle authentications and the connection to the Twitter Streaming API.
        listener = TwitterListener(tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line handle filter the tweets by a keyword list
        stream.filter(track=hash_tag_list)

# # # TWITTER STREAM LISTENER # # #
class TwitterListener(StreamListener):
    # This is a basic listener class that just prints received tweets to stout.

    def __init__(self, tweets_filename):
        self.tweets_filename = tweets_filename

    def on_data(self, data):
        try:
            #gravando os dados
            with open("AllTweets.json", 'a') as tf:
                tf.write(data)
            with open(self.tweets_filename, 'w') as tf:
                tf.write(data)
            #pegando o json
            tweet = json.loads(open(self.tweets_filename).read())
            print(tweet["text"] + " " + str(tweet["id"]))
            #separando o tweet
            champion = tweet["text"].split()
            champion = champion[1]
            #procurando o champion
            organizer = LolaOrganizer("20180909LoLA.json")
            tweets = organizer.champion_search(champion)
            #invertendo a ordem do tweets, remover isso qd conseruir da reply no peply pq ai fica uma escadinha bonitinha
            tweets = tweets[::-1]
            #autenticando na api
            api = API(TwitterAuthenticator().authenticate_twitter_app())
            #setando campo para reply
            reply_helper = "@%s " % (tweet["user"]["screen_name"])
            #dando tweets de reply
            for tweet_text in tweets:
                status = api.update_status(reply_helper + tweet_text, in_reply_to_status_id = tweet["id"])
                print (status)
            """
            reply_helper = "@%s " % (tweet["user"]["screen_name"])
            num = 0


            for tweet_text in tweets:
                if num == 0:
                    status = api.update_status(reply_helper + tweet_text, in_reply_to_status_id = tweet["id"])
                    id = status["id"]
                    num += 1
                    reply_helper += "@%s " % (status["user"]["screen_name"])
                else:
                    status = api.update_status(reply_helper + tweet_text, in_reply_to_status_id = id)
                    id = status["id"]

            """
            print(tweets)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limits occurs.
            return False
        print(status)

def main():
    hash_tag_list = ["#AskLolaBot"]
    tweets_filename = "MostRecentTweet.json"
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(tweets_filename, hash_tag_list)

    
if __name__ == "__main__":
    main()
