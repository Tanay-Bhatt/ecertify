from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail, Message
import os
app = Flask(__name__)
mail= Mail(app)



app.config["ADMINHOME"] = "/admin"
app.config["WEBHOME"] = "/"
app.config["SQLALCHEMY_DATABASE_URI"] = "DATABASE_CONNECTION_STRING"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'SMTP_USERNAME'
app.config['MAIL_PASSWORD'] = 'SMTP_PASSWORD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)

from admin import routes as admin_routes
from admin import models
