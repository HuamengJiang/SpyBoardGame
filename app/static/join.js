$(document).ready(function(){
	update_status();
    setInterval(update_status, 5000);
});

function update_status(){
	$.ajax({
		url: "/update",
		success: function(result){
			var game = JSON.parse(result)
			// alert(game["players"]);
			if (game["players"]){
				$("#player_list").text(game["players"].join(","));
			}
		}
	});
}