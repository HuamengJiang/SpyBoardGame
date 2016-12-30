$(document).ready(function(){
    // setInterval(update_status, 5000);
});

function update_status(){
	$.ajax({
		url: "/update",
		success: function(result){
			
		}
	});
}