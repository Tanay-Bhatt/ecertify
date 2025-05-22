
let download_pdf = document.querySelector("#downloadpdf")
let download_png = document.querySelector("#downloadpng")
let download_jpg = document.querySelector("#downloadjpg")
let image_string = document.querySelector(".certificate-img img").getAttribute("src")
let name = document.querySelector("#username").value




const download_certificate_png = (e)=> {
	let link = document.createElement("a");
	link.style.display = "none";
	link.download = name + "." + "png";
	link.href = image_string;
	link.click();
	link.remove();
}

const download_certificate_jpg = (e)=> {
	let canvas = document.createElement('canvas');
	let image = document.querySelector(".certificate-img img");
	canvas.height = image.naturalHeight;
	canvas.width = image.naturalWidth;
	let ctx = canvas.getContext('2d');
	ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
	let link = document.createElement("a");
	link.style.display = "none";
	link.download = name + "." + "jpg";
	link.href = canvas.toDataURL('image/jpg');
	link.click();
	link.remove();
	canvas.remove();
}


download_pdf.onclick = function() {
	let image = document.querySelector(".certificate-img img");
	let canvas = document.createElement('canvas');
	canvas.height = image.naturalHeight;
	canvas.width = image.naturalWidth;
	let ctx = canvas.getContext('2d');
	ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
	let pdf = new jsPDF('l', 'mm', 'a4');
   pdf.addImage(canvas.toDataURL(), "PNG", 0, 0, pdf.internal.pageSize.getWidth(), pdf.internal.pageSize.getHeight());
  	canvas.remove();
  	pdf.save(`${name}.pdf`);
}

download_png.addEventListener("click", download_certificate_png)
download_jpg.addEventListener("click", download_certificate_jpg)


 if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}