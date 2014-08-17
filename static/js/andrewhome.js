var birthday = new Date(1991,4,23,10,4);

$(document).ready(function() {
	function updateMessage() {
		var ageInMs = Date.now() - birthday;
		var ageInYrs = (ageInMs/1000/3600/24/365).toFixed(9);
		$('#age').text(ageInYrs);
	}
	setInterval(updateMessage, 30);
});



