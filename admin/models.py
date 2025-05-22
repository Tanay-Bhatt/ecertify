import datetime
from operator import and_, or_
from app import app, db
import base64
import os
from scripts.password import hash_password
import bcrypt
# from sqlalchemy.dialects.mysql import LONGTEXT


user_field_size = {
    'username_min': 4,
    'username_max': 24,
    'name_min': 4,
    'name_max': 60,
    'email_min': 6,
    'email_max': 60,
    'password_min': 6,
    'password_max': 60,
    'role': 64
}


class CertifyUser(db.Model):
	__tablename__ = "certify_users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(user_field_size['username_max']), unique=True, index=True)
	name = db.Column(db.String(user_field_size['name_max']))
	password = db.Column(db.LargeBinary(user_field_size['password_max']))
	email = db.Column(db.String(user_field_size['email_max']), unique=True)
	phone_num = db.Column(db.String(20), unique=True)
	date_added = db.Column(db.DateTime)
	date_modified = db.Column(db.DateTime, onupdate=datetime.datetime.now())
	role = db.Column(db.String(user_field_size['role']))
	certificates = db.relationship('CertifyCertificates',primaryjoin="CertifyUser.id == CertifyCertificates.user_id")
	token = db.Column(db.String(32), index=True, unique=True)
	token_expiration = db.Column(db.DateTime)

	def __init__(self, username, name, password, email, phone_num, date_added, role):
		# self.id = id
		self.username = username
		self.name = name
		self.password = password
		self.email = email
		self.phone_num = phone_num
		self.date_added = date_added
		# self.date_modified = date_added
		self.role = role
		# self.certificates = certificates
		# self.token = token
		# self.token_expiration = token_expiration
	
	# def is_admin(self):
	# 	if (self.role == "admin"):
	# 		return True
	# 	else:
	# 		return False

	def validate_admin(token = None):
		if token == None:
			return False
		user = CertifyUser.query.filter_by(token=token).first()
		if user == None:
			return False
		if user and user.token_expiration > datetime.datetime.utcnow() and user.role == "admin":
			return True
		else:
			return False
	
	def login_admin(username, password):
		user = CertifyUser.query.filter_by(username = username).first()
		if user == None:
			return False
		if user.role == "admin" and bcrypt.hashpw(password.encode('utf-8'), user.password) == user.password:
			user.token = base64.b64encode(os.urandom(24)).decode('utf-8')
			user.token_expiration = datetime.datetime.utcnow() + datetime.timedelta(days=15)
			db.session.commit()
			return user.token

	def revoke_token(token):
		user = CertifyUser.query.filter_by(token = token).first()
		if user != None:
			user.token = ""
			db.session.commit()

	def get_last_userid():
		user = CertifyUser.query.all()[-1]
		return user.id

	def email_exists(email):
		user = CertifyUser.query.filter_by(email = email).first()
		if user == None:
			False
		else:
			return True

	def phone_exists(phone):
		user = CertifyUser.query.filter_by(phone_num = phone).first()
		if user == None:
			False
		else:
			return True

	def get_students(page):
		students = CertifyUser.query.filter_by(role = "student").all()[page*10 - 10 : page*10]
		return students

    

class CertifyCertificates(db.Model):
	__tablename__ = 'certify_certificates'
	id = db.Column(db.Integer,primary_key=True,nullable=False)
	user_id = db.Column(db.Integer,db.ForeignKey(CertifyUser.id))
	image = db.Column(db.String(200))
	date = db.Column(db.DateTime, default=datetime.datetime.now())

	def __init__(self, user_id, image):
		self.user_id = user_id
		self.image = image

	def get_certificates(page):
		certificates = CertifyCertificates.query.join(CertifyUser, CertifyCertificates.user_id == CertifyUser.id).add_columns(CertifyCertificates.id, CertifyUser.username, CertifyUser.name, CertifyUser.email).order_by(CertifyCertificates.id.desc()).all()[page*10 - 10 : page*10]
		return certificates

class CertifyTemplates(db.Model):
	__tablename__ = "certify_templates"
	id = db.Column(db.Integer,primary_key=True,nullable=False)
	template_src = db.Column(db.String(1000))
	template_name = db.Column(db.String(200))
	template_color = db.Column(db.String(100))
	date_added = db.Column(db.DateTime, default=datetime.datetime.now())

	def __init__(self, src, name, color):
		self.template_src = src
		self.template_name = name
		self.template_color = color

class CertifyDescriptionTemplates(db.Model):
	__tablename__ = "certify_description_templates"
	id = db.Column(db.Integer,primary_key=True,nullable=False)
	description = db.Column(db.Text())
	date_added = db.Column(db.DateTime, default=datetime.datetime.now())

	def __init__(self, description):
		self.description = description



app.app_context().push()
db.create_all()

