jQuery(function($){







	/*This javascript object holds a bunch of functions that 
	will be used to perform various animations on the landing page*/
	var landing_animate = {
		has_morphed_to_home: false,
		fadeForeground: function(){
						this.has_morphed_to_home = true;
						$("#front_text").animate({ opacity: 0},2500)
						},
		showMainDouble: function(){
					     $('#double_text').animate({ opacity: 1,},5000);
					     $('#double_text').css({"z-index": 1});
						},
		showEnter: function(){$("#enter").animate({ opacity: 1},1250)},
		afterBackground: function(){
					$("#intro").animate({ opacity: 1},1500,this.showEnter);
				}
	}	



	$("#intro, #enter, #back_text, #double_text").css({ opacity: 0});

	landing_animate.afterBackground();



	$("#aenter").hover(
	  function () {
		$("#intro").css({color: '#000000'});
		$('#intro').css('textShadow','#FF0000 4px 4px 4px');

		$("#aenter").css({color: '#000000'});
		$('#aenter').css('textShadow','#FF0000 4px 4px 4px');
		$("span#enter").css({background: '#000000'});
		$("body").css({background: '#000000'});
		},
	  function () {
	  	/*This ensures that if a transition has started there is no need to 
	  	go back to the original background*/
	  	
		if (!landing_animate.has_morphed_to_home)
		{
			$("#intro").css({color: '#FFFFFF'});
			$('#intro').css('textShadow','#000000 4px 4px 4px');
			$('#aenter').css('textShadow','#000000 4px 4px 4px');

			$("span#enter").css({background: '#FFFFFF'});
			$("#aenter").css({color: '#FFFFFF'});
			$("body").css({background: '#FFFFFF'});
		}
	  }
	);

	$("#aenter").click(
	  function (e) {
		e.preventDefault();
		$("body").css({"background-color":'#000000'});
		landing_animate.fadeForeground();
		landing_animate.showMainDouble();
	  }
	);
		});