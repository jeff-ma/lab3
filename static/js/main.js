$(document).ready(function(){
	// SlideToggle url listing details and alter class to change chevron glyphicon to up
	$(".glyphicon-chevron-down").click(function() {
		$(this).parent().siblings().slideToggle();
		$(this).toggleClass("glyphicon-chevron-down glyphicon-chevron-up");
	});

	// SlideToggle url listing details and alter class to change chevron glyphicon to down
	$(".glyphicon-chevron-up").click(function() {
		$(this).parent().siblings().slideToggle();
		$(this).toggleClass("glyphicon-chevron-up glyphicon-chevron-down");
	});

	// Shows the first url listing detail
	$(".url-listing-details:first").show(function() {
		$(this).siblings().children(".glyphicon-chevron-down").toggleClass("glyphicon-chevron-down glyphicon-chevron-up");
	});

	// Check input field for a valid url address and allow submission or else prevent submission and display error message
	$("form").submit(function(e){
		var expression = /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/g;
		if(!expression.test($("#input-field").val())){
			e.preventDefault();
			$("#input-message").html("Hmmm.... Doesn't seem like a valid URL address"); 
		} else{
			$("form").unbind("submit");
			$("#loader").fadeIn(2000);
		}
	});
});