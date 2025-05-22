from flask import (
	render_template,
	request,
	redirect,
	url_for,
	make_response
)
from app import app, db, mail
from . import models 
from datetime import datetime
from scripts.password import hash_password
import csv
from flask_mail import Message
import base64
import os

BASE_URL = "BASEURLHERE"

@app.route(app.config["ADMINHOME"])
def admin_home():
	auth_cookie = request.cookies.get('auth')
	if models.CertifyUser.validate_admin(auth_cookie):
		num_certificates = len(models.CertifyCertificates.query.all())
		num_students = len(models.CertifyUser.query.filter_by(role = "student").all())
		num_templates = len(models.CertifyTemplates.query.all())
		certificates = models.CertifyCertificates.query.join(models.CertifyUser, models.CertifyCertificates.user_id == models.CertifyUser.id).add_columns(models.CertifyCertificates.id, models.CertifyUser.name, models.CertifyUser.email).order_by(models.CertifyCertificates.id.desc()).all()
		if len(certificates) > 10:
			certificates = certificates[0:10]
		return render_template(
			"admin/admin.html", 
			title = "E Certify - Admin",
			num_templates = num_templates,
			num_certificates = num_certificates,
			num_students = num_students,
			certificates = certificates,
			base_url = BASE_URL)
	else:
		return redirect(app.config["ADMINHOME"] + "/login")

@app.route(app.config["ADMINHOME"] + "/login", methods=["GET", "POST"])
def admin_login():
	if models.CertifyUser.validate_admin(request.cookies.get('auth')):
		return redirect(url_for("admin_home"))

	if request.method == "GET":
		return render_template("admin/admin_login.html")

	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")
		validation = models.CertifyUser.login_admin(
			username = username, 
			password = password)
		if validation == False or validation == None:
			return render_template("admin/admin_login.html", error = True)
		else:
			res = make_response(render_template('admin/admin_cookie.html'))  
			res.set_cookie('auth', validation)
			return res

@app.route(app.config["ADMINHOME"] + "/logout")
def logout():
	auth_cookie = request.cookies.get('auth')
	if not models.CertifyUser.validate_admin(auth_cookie):
		return redirect(url_for("admin_login"))
	models.CertifyUser.revoke_token(auth_cookie)
	return redirect(url_for('admin_login'))

@app.route(app.config["ADMINHOME"] + "/add-student", methods=["GET", "POST"])
def add_student():
	auth_cookie = request.cookies.get('auth')
	if not models.CertifyUser.validate_admin(auth_cookie):
		return redirect(url_for("admin_login"))
	if request.method == "GET":
		return render_template(
			"admin/add_student.html", 
			title = "E-Certify - Add Student",
			page = "add-student",
			base_url = BASE_URL)
	if request.method == "POST":
		type = request.form.get("type")
		if type == "form":
			name = request.form.get("name")
			email = request.form.get("email")
			phone = request.form.get("number")
			message = ""
			if models.CertifyUser.email_exists(email):
				message = "Email Already Exists"
			elif models.CertifyUser.phone_exists(phone):
				message = "Phone Number Already Exists"
			else:
				register = models.CertifyUser(
					username = "".join(name.split(" ")) + str(models.CertifyUser.get_last_userid()),
					name = name,
					password = hash_password("student123"),
					phone_num = phone,
					email = email,
					date_added = datetime.now(),
					role = "student"
				)
				db.session.add(register)
				db.session.commit()
				message = "User registered successfully"
			return render_template(
			"admin/add_student.html", 
			title = "E-Certify - Add Student",
			page = "add-student",
			message = message,
			base_url = BASE_URL)
		if type == "csv":
			file = request.files["file"]
			f_string = file.stream.read()
			f_string = f_string.decode('utf-8')
			data = [{k: v for k, v in row.items()} for row in csv.DictReader(f_string.splitlines(), skipinitialspace=True)]
			count=0
			count_line=0
			created_lines=[]
			line=[]
			try:
				if file.filename != '':
					for item in data:
						name = item["name"]
						email = item["email"]
						phone = item["phone"]
						try:
							register = models.CertifyUser(
								username = "".join(name.split(" ")) + str(models.CertifyUser.get_last_userid()),
								name = name,
								password = hash_password("student123"),
								phone_num = phone,
								email = email,
								date_added = datetime.now(),
								role = "student"
							)
							db.session.add(register)
							db.session.commit()
							count += 1
						except:
							pass
			except:
				pass
			return render_template(
				"admin/add_student.html", 
				title = "E-Certify - Add Student",
				page = "add-student",
				message = f"{count} students uploaded from file",
				base_url = BASE_URL)

@app.route(app.config["ADMINHOME"] + "/all_students", methods=["GET"])
@app.route(app.config["ADMINHOME"] + "/all_students/<int:page>", methods=["GET"])
def all_students(page=1):
	if not models.CertifyUser.validate_admin(request.cookies.get('auth')):
		return redirect(url_for("admin_login"))
	students = models.CertifyUser.get_students(page)
	total_students = float(len(models.CertifyUser.query.filter_by(role = "student").all())/10)
	if (not total_students.is_integer()):
		total_students += 1
	total_students = int(total_students)
	return render_template(
		"admin/students.html",
		students = students,
		len_students = total_students,
		page = page,
		title = "E-Certify - Students",
			base_url = BASE_URL)	

@app.route(app.config["ADMINHOME"] + '/student/<username>', methods=["GET", "POST"])
def student(username):
	if not models.CertifyUser.validate_admin(request.cookies.get('auth')):
		return redirect(url_for("admin_login"))
	if request.method == "GET":
		user = models.CertifyUser.query.filter_by(username = username).first()
		if user == None:
			message = "No Student Found"
			return render_template(
				"admin/student.html",
				title = "E-Certify - Student",
				message = message,
			base_url = BASE_URL)
		return render_template(
			"admin/student.html",
			title = "E-Certify - Student",
			user = user,
			base_url = BASE_URL)
	if request.method == "POST":
		name = request.form.get("name")
		email = request.form.get("email")
		phone = request.form.get("phone")
		user = models.CertifyUser.query.filter_by(username = username).first()
		message = ""
		if models.CertifyUser.email_exists(email) and user.email != email:
			message = "Email Already Exists"
		elif models.CertifyUser.phone_exists(phone) and user.phone_num != phone:
			message = "Phone Number Already Exists"
		else:
			user.name = name
			user.email = email
			user.phone_num = phone
			message = "User updated successfully"
			db.session.commit()
		return render_template(
			"admin/student.html",
			title = "E-Certify - Student",
			message = message,
			user = user,
			base_url = BASE_URL)

@app.route(app.config["ADMINHOME"] + '/student/delete/<username>', methods=["GET", "POST"])
def delete_student(username):
	if not models.CertifyUser.validate_admin(request.cookies.get('auth')):
		return redirect(url_for("admin_login"))
	student = models.CertifyUser.query.filter_by(username = username).delete()
	db.session.commit()
	return redirect(url_for("all_students"))

@app.route(app.config["ADMINHOME"] + '/templates')
def templates():
	if not models.CertifyUser.validate_admin(request.cookies.get('auth')):
		return redirect(url_for("admin_login"))
	certificates = models.CertifyTemplates.query.all()
	return render_template(
		"admin/template.html",
		templates = certificates,
		title = "E-Certify - Certificate Templates",
			base_url = BASE_URL)

@app.route(app.config["ADMINHOME"] + '/generate-certificate/<int:id>')
def generate_certificate(id):
	if not models.CertifyUser.validate_admin(request.cookies.get('auth')):
		return redirect(url_for("admin_login"))
	certificate = models.CertifyTemplates.query.filter_by(id = id).first()
	students = models.CertifyUser.query.filter_by(role="student").order_by(models.CertifyUser.name).all()
	student_details = [{"username" : student.username, "name" : student.name} for student in students]
	try:
		cid = models.CertifyCertificates.query.all()[-1].id + 1
	except:
		cid = 1
	return render_template(
		"admin/generate_certificate.html",
		certificate = certificate,
		student_details = student_details,
		cid = cid,
		title = "E-Certify - Generate Certificate",
			base_url = BASE_URL)

@app.route(app.config["ADMINHOME"] + "/all-certificates", methods=["GET"])
@app.route(app.config["ADMINHOME"] + "/all-certificates/<int:page>", methods=["GET"])
def all_certificates(page=1):
	if not models.CertifyUser.validate_admin(request.cookies.get('auth')):
		return redirect(url_for("admin_login"))
	certificates = models.CertifyCertificates.get_certificates(page)
	total_certificates = float(len(models.CertifyCertificates.query.all())/10)
	if (not total_certificates.is_integer()):
		total_certificates += 1
	total_certificates = int(total_certificates)
	return render_template(
		"admin/certificates.html",
		certificates = certificates,
		len_certificates = total_certificates,
		page = page,
		title = "E-Certify - Certificates",
			base_url = BASE_URL)	

@app.route(app.config["ADMINHOME"] + "/publish-certificate", methods=["POST", "GET"])
def publish_certificate():
	if request.method == "GET":
		return redirect(url_for('admin_home'))
	if not models.CertifyUser.validate_admin(request.cookies.get('auth')):
		return redirect(url_for("admin_login"))
	username = request.form.get("formuserid")
	image = request.form.get("formimage")
	try:
		cid = models.CertifyCertificates.query.all()[-1].id + 1
	except:
		cid = 1
	user = models.CertifyUser.query.filter_by(username = username).first()
	image_name = f"{user.username}_{cid}.png"
	with open(f"{os.getcwd()}/static/uploads/{image_name}" , "wb") as img:
		img.write(base64.decodebytes(image.replace("data:image/png;base64,", "").encode())) 
	register = models.CertifyCertificates(
		user_id = user.id,
		image = image_name)
	db.session.add(register)
	db.session.commit()
	certificate = models.CertifyCertificates.query.filter_by(id = cid).first()
	message = f"""
Dear {user.name},
Congratulations on receiving your event certificate from E-Certify.

You can find your certficate attached in png format in this mail.
To verify the authenticity of your certificate, please follow this verification link {BASE_URL}/verify/{certificate.id} . This link will take you to the verification page
"""
	message_admin = f"""
Dear Admin,
A new certficate for {user.name} with user id {user.id} is generated. The certificate id is {certificate.id}.
A copy of generated certificate is attached in this email. 
Verification link : {BASE_URL}/verify/{certificate.id}
"""
	try:
		admin = models.CertifyUser.query.filter_by(role="admin").first()
		msg = Message("E-Certify", sender = 'tanayb755@gmail.com', recipients = [user.email])
		msg.body = message
		# data_bytes = base64.b64encode(image)
		data_bytes = base64.decodebytes(image.replace("data:image/png;base64,", "").encode())
		msg.attach("certificate.png", "image/png", data_bytes)
		mail.send(msg)
		msg = Message("E-Certify", sender = 'tanayb755@gmail.com', recipients = [admin.email])
		msg.body = message_admin
		msg.attach("certificate.png", "image/png", data_bytes)
		mail.send(msg)
	except Exception as e:
		print(e)
		pass
	return render_template(
		"admin/certificate_generated.html",
		image = image_name,
		user = user,
		certificate = certificate,
		title = "E-Certify - Certificate Generated",
		message = f"Certificate mailed to {user.email}, {admin.email}",
			base_url = BASE_URL)


@app.route("/")
def webapp_home():
	return render_template(
			"webapp/index.html",
			title = "E-Certify")
	

@app.route('/verification', methods=["POST"])
def verification():
	cid = request.form.get("cid")
	certificate = models.CertifyCertificates.query.filter_by(id = cid).first()
	if certificate == None:
		return render_template(
			"webapp/verification.html", 
			isvalid = 0)
	user = models.CertifyUser.query.filter_by(id = certificate.user_id).first()
	return render_template(
		"webapp/verification.html",
		isvalid = 1,
		certificate = certificate,
		user = user)


@app.route('/verify/<int:cid>', methods=["GET"])
def verify(cid):
	certificate = models.CertifyCertificates.query.filter_by(id = cid).first()
	if certificate == None:
		return render_template(
			"webapp/verification.html", 
			isvalid = 0)
	user = models.CertifyUser.query.filter_by(id = certificate.user_id).first()
	return render_template(
		"webapp/verification.html",
		isvalid = 1,
		certificate = certificate,
		user = user)


@app.route('/add-templates', methods=["GET"])
def add_templates():
    existing_templates = [t.template_name for t in models.CertifyTemplates.query.all()]
    added_count = 0

    for i in range(1, 9):
        template_name = f'template{i}'
        if template_name in existing_templates:
            continue

        src = url_for('static', filename=f'assets/certificates/template{i}.png')
        color = '#222222'

        new_template = models.CertifyTemplates(
            src=src,
            name=template_name,
            color=color
        )
        db.session.add(new_template)
        added_count += 1

    db.session.commit()
    return f"Success: {added_count} templates added"
