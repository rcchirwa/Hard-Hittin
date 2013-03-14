import tweepy
import json
import urllib2
import time
import miscUtils
from collections import namedtuple
import logging
import api_keys
 
#my keys pulled from a file which is git ignored
#use you ow keys here
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

	results = api.user_timeline("HardHittin508");

	Tweet = namedtuple('Tweet','screen_name, text, profile_image_url,id,created_at_time,created_at_epoch,time_lapsed')

	ids = []
	tweets = []

	for result in results:	
		date_time = '2007-02-05 16:15:18'
		date_time = '%s-%s-%s %s'  % (result.created_at.year,result.created_at.month,result.created_at.day,result.created_at.time())
		pattern = '%Y-%m-%d %H:%M:%S'
		epoch = int(time.mktime(time.strptime(date_time, pattern)))

		tweet = Tweet(result.author.screen_name, result.text, result.user.profile_image_url, result.id, date_time, epoch,'')

		tweets.append(tweet)

		timenow = int(time.time())

	return tweets


def addLapsedTime(tweet):
	upDatedTweet = namedtuple('Tweet','screen_name, text, profile_image_url,id,created_at_time,created_at_epoch,time_lapsed')
	time_lapsed = miscUtils.time_lapse(tweet.created_at_epoch)
	updatedTweet = upDatedTweet(tweet.screen_name, tweet.text, tweet.profile_image_url, tweet.id, tweet.created_at_time, tweet.created_at_epoch, time_lapsed)
	return updatedTweet



def getModTweets():
	return map(addLapsedTime,getTweets())


def getJson(total=-1):

	tweets_out = []

	tweets = getModTweets()

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
		a = json.dumps(tweets_out[0:total-1])
	else:
		a = json.dumps(tweets_out)

	return a