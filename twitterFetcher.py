import tweepy, re, json, operator
from tweepy import Stream
from tweepy.streaming import StreamListener


#auth information for Twitter API
consumer_key = 'uVDSBEX1VwUfxIYrOL2iRMeU6'
consumer_secret = 'huPAfnHiVs5SFb97eaeJp2OF7SPsIt0RWBsI0UujKq8JYvX9G3'
access_token = '805801320-GHQc338xf3BEpihbWHWSm2oNyvl3WwikTcPrWt2A'
access_token_secret = 'TOyA8yRvyFQEnl1xq3VTinKnASHFT0EYoQpbVwSKvNoA1'
#Tweepy Handler for accessing Oauth and Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#streaming API
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('blizz2.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['@DustinBrowder'])
#---------