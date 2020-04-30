async function PullBackground() {
	let c = ['au', 'ca', 'cn', 'de', 'fr', 'jp', 'us', 'gb'][Math.floor(Math.random()*8)]
	var json = await (await fetch(`https://peapix.com/bing/feed?country=${c}`)).json()
	document.body.style.backgroundImage = "url("+ json[0].fullUrl +")"
	document.body.style.backgroundSize = "100%";
}

// postition won't work correctly if you
// use a custom userChrome.css that modifies
// the browsers default content display.
// UI mods should not affect it.
$(document).ready(function() {
	PullBackground();
	$( "#container" ).draggable().position({
	my: "center",
	at: "center",
	of: window
	});
});

// Need to update this to reposition on window resize !!
// Might not be needed, as its going to be dragged anyway.
