function set_active_tab(tab) {
	
	let tab_list = document.getElementById("tabs-bar").getElementsByTagName("ul")[0];
	for (let i = 0; i < tab_list.getElementsByTagName("li").length; i += 1) {
		if (tab == i) {
			tab_list.getElementsByTagName("li")[i].classList.add("active");
			continue;
		}
		tab_list.getElementsByTagName("li")[i].classList.remove("active");
	}
	scroll_to_tab(tab);
	update_categories(tab_list.getElementsByTagName("li")[tab].textContent.trim());
}

function scroll_to_tab(tab) {
	
	let tab_bar = document.getElementById("tabs-bar").getElementsByTagName("ul")[0];
	let sample_tab = tab_bar.getElementsByClassName("tab")[0];
	tab_bar.scrollTo((tab-1) * (Number(window.getComputedStyle(sample_tab).width.slice(0, -2)) + Number(window.getComputedStyle(sample_tab).getPropertyValue("margin-left").slice(0, -2))), 0);
}

function update_categories(year) {
	
	window.history.pushState({}, "", window.location.href.split("?")[0] + "?year=" + year);

	let request = new XMLHttpRequest();
	request.open("GET", window.location.href, false);
	request.send();
	
	let new_categories = (new DOMParser()).parseFromString(request.responseText,"text/html").getElementById("tabs-display-content").innerHTML;
	document.getElementById("tabs-display-content").innerHTML = new_categories;
}