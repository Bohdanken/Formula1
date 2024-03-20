function update_profile(tab) {
	let username = tab.textContent.trim();
	window.history.pushState({}, "", window.location.href.split("?")[0] + "?profile=" + username);

	let request = new XMLHttpRequest();
	request.open("GET", window.location.href, false);
	request.send();
	
	let new_profile = (new DOMParser()).parseFromString(request.responseText,"text/html").getElementById("tabs-display-content").innerHTML;
	document.getElementById("tabs-display-content").innerHTML = new_profile;
}