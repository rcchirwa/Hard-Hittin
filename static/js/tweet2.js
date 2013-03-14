	$(function(){


	  var Tweet = Backbone.Model.extend({
			urlRoot : '/tweet.json'
	  });


	  var Tweets = Backbone.Collection.extend({
			model: Tweet,
			url: '/tweets.json'
	  });

	  var TweetView = Backbone.View.extend({
	    	tagName: 'li',
			className: 'tweet',

	    	template: _.template(
			"	<header class=\"group\">	" +
			"		<span class=\"tweet_image\">	" +
			"			<img src=\"<%= profile_image_url %>\">	" +
			"		</span>	" +
			"		<span class=\"tweet_screen_name\">	" +
			"			<a href=\"https://twitter.com/<%= screen_name%>\"> @<%= screen_name%></a>	" +
			"		</span>	" +
			"	</header>	" +
			"	<br>	" +
			"	<section class=\"tweet_text\">	" +
			"		<%= text %>	" +
			"	</section>	" +
			"	<br>	" +
			"	<footer>	" +
			"		<span>	" +
			"			<img src=\"../images/twitter-bird-light-bgs.png\" height=\"20\" width=\"20\">	" +
			"		</span>	" +
			"		<span>	" +
			"			<%= time_lapsed %>	" +
			"		</span>	" +
			"	</footer>	"
			),


		initialize: function(){
			_.bindAll(this, 'render','update'); // every function that uses 'this' as the current object should be in here
			this.model.on('change', this.update);
			this.render();	
		},

    	render: function(){;
			$(this.el).append(this.template(this.model.toJSON()));
			return this; // for chainable calls, like .render().el
    	},

    	update: function(){;
			$(this.el).html(this.template(this.model.toJSON()));
			return this; // for chainable calls, like .render().el
    	}

	  });


	var TodoListView = Backbone.View.extend({
		el: $('ul#main_tweet'),
		initialize: function(){
			this.collection.on('add', this.addOne, this);
			this.collection.on('reset', this.addAll, this);
		},
		addOne: function(todoItem){
			var tweetView = new TweetView({model: todoItem});
			this.$el.append(tweetView.update().el);
		},
		addAll: function(){
			this.collection.forEach(this.addOne, this);
		},
		render: function(){
			this.addAll();
		}
	});

	var tweets2 = new Tweets();	

	
	var todoListView = new TodoListView({
			collection: tweets2
		});


	var tweets_on_site = 0;	


	tweets2.fetch(
		{
    	success: function(collection, response){
        		tweets_on_site = tweets_on_site + tweets2.length;
    		}
    	}
    	);


	$('#Next').click(function(){sweep('-=');});
	$('#Previous').click(function(){sweep('+=');});




	/*track that current position of the slider*/
	var slider_index = 0;
	
	/*how many tweets have been recovered from the server
	this will be used later when iterating through diffrent viewport 
	sizes that use different frames .*/
	var tweets_seen = 0;


	var sweep = function(direction){

			/*the figure below computes the number of tweets on the screen*/
			var frame_size = 0;

			/*current width of the individual tweets this is the full box*/
			var current_tweet_width = parseInt($('.tweet:first').outerWidth(true),10)

			/*this is the lnegth of the total tweet frame*/
			var tweets_frame_width = parseInt($('#tweets_frame').width());

			/*compute the number of tweets that can fit snug on the screen
			then take the floor of that*/
			frame_size = Math.floor(tweets_frame_width/current_tweet_width);



			/*compute values and update variables based on the direction */
			if (direction == '+=')
			{
				if (slider_index == 0){
					return;
				}
				else
					slider_index += 1;
			}
			else
				slider_index -= 1;
			  
			/*compute the size of the sweep*/
			var width = parseInt($('.tweet:first').outerWidth(true),10)*frame_size;
						
 
			$('ul#main_tweet').queue(function(next){
				$(this).animate(
					{'margin-left': direction+width},
					{
						duration: 1000
					}
				);
				next();
			});
		}/*end sweep function*/

	})/*end jquery*/







