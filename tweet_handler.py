import tweepy
import json
import urllib2
import time
import miscUtils
from collections import namedtuple
import api_keys
 



#my keys pulled from a file which is git ignored
twitter_keys = api_keys.twitter_keys

access_token = twitter_keys['access_token'] 
access_token_secret =  twitter_keys['access_token_secret']

consumer_key = twitter_keys["consumer_key"]
consumer_secret = twitter_keys["consumer_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def getTweets():
	tweets = []



	#set the time line that we are interested
	results = api.user_timeline("HardHittin508");


	#create a nametuple for the fields the we are interested in 
	Tweet = namedtuple('Tweet','screen_name, text, profile_image_url,id,created_at_time,created_at_epoch,time_lapsed')


	#collection to store the tweets
	#explore using a key value pair structure
	tweets = []

	for result in results:	

		#creation information
		date_time = '%s-%s-%s %s'  % (result.created_at.year,result.created_at.month,result.created_at.day,result.created_at.time())

		pattern = '%Y-%m-%d %H:%M:%S'

		#compute the related epoch
		epoch = int(time.mktime(time.strptime(date_time, pattern)))

		#populate the tweets tuple
		tweet = Tweet(result.author.screen_name, result.text, result.user.profile_image_url, result.id, date_time, epoch,'')

		#append the tweet to our collection
		tweets.append(tweet)

		#timenow = int(time.time())

	return tweets




'''
	This takes a tweet and returns 
	a tuple that has the time lapsed since the tweet was generated. 
	NOTE: explore moving this to the front end to the backbones moule
'''
def addLapsedTime(tweet):
	upDatedTweet = namedtuple('Tweet','screen_name, text, profile_image_url,id,created_at_time,created_at_epoch,time_lapsed')
	
	time_lapsed = miscUtils.time_lapse(tweet.created_at_epoch)
	
	updatedTweet = upDatedTweet(tweet.screen_name, tweet.text, tweet.profile_image_url, tweet.id, tweet.created_at_time, tweet.created_at_epoch, time_lapsed)
	return updatedTweet

'''
	This take a collection of tweets and the maps then to compute time lapsed since the tweet was created. 
'''
def getModTweets():
	return map(addLapsedTime,getTweets())



'''
	convert the colection of tweets to json object to be used
	to interact with the browser via a js libraries
	total is the number of tweets to return where -1 mean return everything
'''

def getJson(total=-1):

	tweets_out = []

	tweets = getModTweets()
	#temp = 
	for tweet in tweets:
		temp = {}
		temp["screen_name"] = tweet.screen_name
		temp["text"] = tweet.text
		temp["profile_image_url"] = tweet.profile_image_url
		temp["id"] = tweet.id
		temp["created_at_time"] = tweet.created_at_time
		temp["created_at_epoch"] = tweet.created_at_epoch
		temp["time_lapsed"] = tweet.time_lapsed
		tweets_out.append(temp)
	
	if total != -1: 
		a = json.dumps(tweets_out[:(total-1)])
	else:
		a = json.dumps(tweets_out)

	return a