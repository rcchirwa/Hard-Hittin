import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
import jinja2
import webapp2
import re
import miscUtils
import json
from google.appengine.api import memcache
import tweet_handler


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)



#this in the main handler used for rendering/writing input to the browser
#almost all the subsequent classes inherit from this
class Handler(webapp.RequestHandler):
	'''renders html that is passed to the to it is variable a'''	
	def write(self, a, **kw):
		self.response.out.write(a, **kw)


	'''use jinja2 to get the given template and then render it with the given parameters'''
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
 		return t.render(params)


	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class FlushCache(Handler):
	def get(self):
		memcache.flush_all()
		self.redirect("/")

########################################################################################################################################		
class Tweet(Handler):
	def render_front(self):
		tweet_id = self.request.get("id")
		'''logging.info("1 tweet: %s"%tweet)
		logging.info("2 tweet: %s"%tweet)
		logging.info("3 tweet: %s"%tweet)

	
		#logging.info("tweet %s" % len(tweets))
		logging.info("memcache.get('max_id')%s " % memcache.get('max_id'))
		logging.info("memcache.get('tweet_ids')%s " % memcache.get('tweet_ids'))
		logging.info("memcache.get('tweet_ids')%s " % memcache.get('tweet_ids'))'''
	
		tweet_ids = memcache.get('tweet_ids')
		len_tweet_ids = len(tweet_ids)
		var = int(tweet_id) % len_tweet_ids
		logging.info("var tweet len_tweet_ids: %s",var)
		tweet_html = memcache.get(tweet_ids[var])

		logging.info('tweet_html\n\n%s'%tweet_html)

		
		self.write(tweet_html)

	def get(self):
		self.render_front()
			
class Tweets(Handler):
	def render_front(self):
		tweets = tweet_handler.getModTweets()

		self.render("tweets2.html",tweets=tweets[0:5])

	def get(self):
		self.render_front()


class Tweets_to_json(Handler):
	def render_front(self):
		#parameter of -1 indicates that 
		tweets = tweet_handler.getJson(-1)

		self.response.headers['Content-Type'] = "application/json; charset=UTF-8"
		logging.info("JSON %s" % tweets)
		self.response.out.write(tweets)

	def get(self):
		self.render_front()



class Tweets_to_json1(Handler):
	def render_front(self):
		tweets = tweet_handler.getJson(-1)

		self.response.headers['Content-Type'] = "application/json"		
		logging.info("JSON %s" % tweets)
		self.response.out.write(tweets)

	def get(self):
		self.render_front()


class Landing(Handler):
	def write_html(self): 
		self.render("landing.html")

	def get(self):		
		self.write_html()



'''
	will eventually be used to integrate souncloud into the page
'''
class Music(Handler):
	def write_html(self,widget=''): 
		self.render("music.html")

	def get(self):
		# create a client object with your app credentials
		#dir(requests)
		'''client = soundcloud.Client(client_id='7901d28344f79bb53d022b8f47f0ac2a')

		track = client.get('/resolve', url='http://soundcloud.com/forss/flickermood')

		logging.info(track.id)



		# get a tracks oembed data
		track_url = 'http://soundcloud.com/forss/flickermood'
		embed_info = client.get('/oembed', url=track_url)

		# render the html for the player widget
		#return render_template('player.html', widget=embed_info['html'])		
		self.write_html(widget=embed_info['html'])'''
		self.write_html()

'''
	This is used to route page that do not have a special url
'''
class Generic_Router(Handler):
	def write_html(self,destination): 
		self.render(destination)

	def get(self):		
		destination= self.request.path.split('/')[1]
		self.write_html(destination)

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
application = webapp2.WSGIApplication([('/', Landing),
				       	('/music.html', Music),
						('/tweets.html', Tweets),
						('/tweets.json', Tweets_to_json),
						('/tweets.json/1', Tweets_to_json1),
					 	('/tweet?(?:[a-zA-Z0-9_-]+/?)*', Tweet),
					 	('/(?:[a-zA-Z0-9_-]+/?).html',  Generic_Router),
                               ],
                              debug=True)
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()