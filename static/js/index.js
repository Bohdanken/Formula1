function update_categories(tab) {
	
	let year = tab.textContent.trim()
	
	window.history.pushState({}, "", window.location.href.split("?")[0] + "?year=" + year);

	let request = new XMLHttpRequest();
	request.open("GET", window.location.href, false);
	request.send();
	
	let new_categories = (new DOMParser()).parseFromString(request.responseText,"text/html").getElementById("tabs-display-content").innerHTML;
	document.getElementById("tabs-display-content").innerHTML = new_categories;
}