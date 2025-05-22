let csv_upload_input = document.querySelector("#csvfile")
let csv_label = document.querySelector("label[for=csvfile]")


const changeLabel = e => {
	csv_label.innerText = csv_upload_input.files[0].name;
}

csv_upload_input.addEventListener("input", changeLabel);