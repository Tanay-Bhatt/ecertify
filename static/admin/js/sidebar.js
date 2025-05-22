// sidebar toggle
console.log(document.querySelectorAll("*"))
let toggle_landscape = document.querySelector("#sidebar-toggle-landscape")
let sidebar_landcape = document.querySelector(".sidebar-landscape")
let main_container = document.querySelector(".main-content")
toggle_landscape.onclick = ()=> {
	if (toggle_landscape.querySelector("i").classList.contains("fa-chevron-right")) {
		sidebar_landcape.style.left = "0";
		toggle_landscape.querySelector("i").classList = "fa fa-chevron-left";
		if (window.matchMedia("(orientation: landscape)").matches) {
			main_container.style.width = "calc(100% - 35vmin)";
			main_container.style.left = "35vmin";
		}
		
	} else {
		sidebar_landcape.style.left = "-28vmin";
		toggle_landscape.querySelector("i").classList = "fa fa-chevron-right";
		if (window.matchMedia("(orientation: landscape)").matches) {
			main_container.style.width = "calc(100% - 7vmin)";
			main_container.style.left = "7vmin";
		}
		
	}
}