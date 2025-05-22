let certificate_type = document.querySelector("#csubhead span")
let certificate_type_input = document.querySelector("input#type")

let name_on_certificate = document.querySelector("#cname")
let name_on_certificate_input = document.querySelector("select#name")

let description = document.querySelector("#cdescription")
let description_input = document.querySelector("textarea#description")

let issuer = document.querySelector("#cissuername")
let issuer_input = document.querySelector("#issuername")

let issuer_desg = document.querySelector("#cissuerdesg")
let issuer_desg_input = document.querySelector("#issuerdesg")

let form_image = document.querySelector("#formimage")
let form_username = document.querySelector("#formuserid")

const updateType = ()=> {
	certificate_type.innerText = certificate_type_input.value;
}

const updateName = ()=> {
	name_on_certificate.innerText = name_on_certificate_input.value.split("||")[1];
	document.querySelector("#formuserid").value  = name_on_certificate_input.value.split("||")[0];
}

const updateDescription = ()=> {
	description.innerText = description_input.value;
}

const updateIssuer = ()=> {
	issuer.innerText = issuer_input.value;
}

const updateIssuerDesg = ()=> {
	issuer_desg.innerText = issuer_desg_input.value;
}


function download_cert() {
	html2canvas(document.querySelector(".certificate-editor .certificate .container")).then(canvas => {
	    document.querySelector(".certificate .certificate-editor").appendChild(canvas)
	    canvas.id = "outputcertificate"
	    var image = canvas.toDataURL("image/" + 'png');
	    let link = document.createElement("a");
	    link.style.display = "none";
	    link.download = name_on_certificate.innerText + "." + "png";
	    link.href = image;
	    link.click();
	    link.remove();
	    canvas.remove();
	});
}

function generate_cert() {
	html2canvas(document.querySelector(".certificate-editor .certificate .container")).then(canvas => {
	    document.querySelector(".certificate .certificate-editor").appendChild(canvas);
	    canvas.id = "outputcertificate";
	    var image = canvas.toDataURL("image/" + 'png');
	   	form_username.value = name_on_certificate_input.value.split("||")[0];
	   	form_image.value = image;
	    canvas.remove();
	    document.querySelector("#generateform").submit()
	});
}

let download = document.querySelector("#download");
let generate = document.querySelector("#generate")

download.onclick = ()=> {
	download_cert()
}

generate.onclick = ()=> {
	generate_cert()
}

document.querySelector("#formuserid").value  = name_on_certificate_input.value.split("||")[0];
certificate_type_input.addEventListener("input", updateType)
name_on_certificate_input.addEventListener("input", updateName)
description_input.addEventListener("input", updateDescription)
issuer_input.addEventListener("input", updateIssuer)
issuer_desg_input.addEventListener("input", updateIssuerDesg)