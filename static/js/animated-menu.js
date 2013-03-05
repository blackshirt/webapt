$(document).ready(function() {
	$("li").mouseover(function(){
		$(this).stop().animate({height:'150px'}, {queue:false, duration:600, easing" 'easeOutBounce'})
	});

	$("li").mouseout(function(){
		$(this).stop().animate({height:'50px'}, {queue:false, duration:600, easing: 'easeOutBounce'});
	});


});
