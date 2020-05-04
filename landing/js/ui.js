async function PullBackground() {
	let c = ['au', 'ca', 'cn', 'de', 'fr', 'jp', 'us', 'gb'][Math.floor(Math.random()*8)]
	var json = await (await fetch(`https://peapix.com/bing/feed?country=${c}`)).json()
	$('#background').attr("src", json[0].fullUrl)
}

async function GetTopSuggestion(seed) {
	let r = await fetch("https://landingautosuggest.cognitiveservices.azure.com/bing/v7.0/suggestions?q="+ seed, {
		"method": "GET",
		"headers": {
			"content-type": "application/json",
			"bingapis-market": "en-UK",
			"ocp-apim-subscription-key": "e0d5e841ab604b6c94bc4aa822b3be00"
		},
	})
	let results = (await r.json()).suggestionGroups[0].searchSuggestions
	results = results.map(r => r.displayText)
	return (results.length) > 0 ? results : []
}

var lastQuery = Date.now() - 2000;
var pv;

const UpdateSearch = async query => {
	let now = Date.now()
	if (now - lastQuery > 1000){
		lastQuery = now
		pv.options = await GetTopSuggestion(query)
	}
	pv.repaint()
	pv.o3DropDown();
}

function HandleEnter() {
	let query = pv.getText()
  var pattern = new RegExp('^(?<protocol>https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
	if (match = query.match(pattern)){
		window.location = (match.groups.protocol) ? '' : 'https://' + query
	} else {
		window.location = 'https://google.com/search?q=' + query
	}
}

function SetupTabCompletion(){
	pv = completely(document.getElementById('search'),{
		backgroundColor:'transparent',
		fontFamily: 'cascadia code, monospace',
		fontSize: '13px',
		color:'#DDDDDD',
		overflow: 'hidden'
	});
	pv.input.focus();
	pv.onChange = UpdateSearch
	pv.onEnter = HandleEnter
}

// postition won't work correctly if you
// use a custom userChrome.css that modifies
// the browsers default content display.
// UI mods should not affect it.
$(document).ready(function() {
	SetupTabCompletion();
	PullBackground();
	$( "#container" ).draggable().position({
	my: "center",
	at: "center",
	of: window
	});
});

// Need to update this to reposition on window resize !!
// Might not be needed, as its going to be dragged anyway.