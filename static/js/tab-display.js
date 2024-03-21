function set_active_tab(tab, update_tabs_content) {
	
	let tab_list = document.getElementById("tabs-bar").getElementsByTagName("ul")[0];
	for (let i = 0; i < tab_list.getElementsByTagName("li").length; i += 1) {
		if (tab == i) {
			tab_list.getElementsByTagName("li")[i].classList.add("active");
			continue;
		}
		tab_list.getElementsByTagName("li")[i].classList.remove("active");
	}
	scroll_to_tab(tab);
	update_tabs_content(tab_list.getElementsByTagName("li")[tab]);
}

function scroll_to_tab(tab) {
	
	let tab_bar = document.getElementById("tabs-bar").getElementsByTagName("ul")[0];
	let sample_tab = tab_bar.getElementsByClassName("tab")[0];
	tab_bar.scrollTo((tab-1) * (Number(window.getComputedStyle(sample_tab).width.slice(0, -2)) + Number(window.getComputedStyle(sample_tab).getPropertyValue("margin-left").slice(0, -2))), 0);
}