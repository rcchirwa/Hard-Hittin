	$(function(){
		/*Backbone.sync = function(method, model, success, error){ 
    	success();
	  }*/


	  var Tweet = Backbone.Model.extend({
			urlRoot : '/tweets.json'
	  });


	  var Tweets = Backbone.Collection.extend({
			model: Tweet,
			url: '/tweets.json'
	  });




	  var TweetView = Backbone.View.extend({
	    	tagName: 'div',
			className: 'tweet',

	    	template: _.template(
			"	<div style=\"display:block\">	" +
			"		<span style=\"float:left\">	" +
			"			<img src=\"<%= profile_image_url %>\">	" +
			"		</span>	" +
			"		<span style=\"float:left; padding:0px 0px 0px 10px;\">	" +
			"			<a href=\"https://twitter.com/<%= screen_name%>\"> @<%= screen_name%></a>	" +
			"		</span>	" +
			"	</div>	" +
			"	<br>	" +
			"	<div style=\"display:block;clear:both;\">	" +
			"		<%= text %>	" +
			"	</div>	" +
			"	<br>	" +
			"	<div style=\"display:block\">	" +
			"		<span style=\"float:left\">	" +
			"			<img src=\"../images/twitter-bird-light-bgs.png\" height=\"20\" width=\"20\">	" +
			"		</span>	" +
			"		<span style=\"float:left\">	" +
			"			<%= time_lapsed %>	" +
			"		</span>	" +
			"	</div>	"
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
		el: $('div#main_tweet'),
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

	tweets2.fetch();


	$('#Next').click(function(){sweep('-=');});
	$('#Previous').click(function(){sweep('+=');});


	var slider_index = 0;


	var sweep = function(direction){
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
			  

			var width = $('.tweet:first').width()*3;
			
 				$('div#main_tweet').queue(function(next){$(this).animate(
						{'left': direction+width},
						{duration: 1000}
						);
						next();
						});
			}

	})







