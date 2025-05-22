# 📜 E-Certify – Certificate Generator & Verifier

[![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)](https://github.com/Tanay-Bhatt) [![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/) [![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask)](https://flask.palletsprojects.com/) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![Status](https://img.shields.io/badge/status-deployed-success)](https://ecertifyapp.pythonanywhere.com/) [![Repo Size](https://img.shields.io/github/repo-size/Tanay-Bhatt/ecertify)](https://github.com/Tanay-Bhatt/ecertify)


E-Certify is a Flask-based web app for managing students, generating certificates from templates, and enabling public verification — with mail support and admin dashboard.

---

## 🌐 Live App

👉 **Live Website**: [https://ecertifyapp.pythonanywhere.com/](https://ecertifyapp.pythonanywhere.com/)  
📺 **Preview Video**: [https://vimeo.com/1086772372](https://vimeo.com/1086772372)

---

## 🚀 Features

🔐 **Admin Authentication**
- Bcrypt-secured login
- Cookie-based sessions
- Role-based access

👨‍🎓 **Student Management**
- Add via form or upload CSV
- Edit, delete, list with pagination

🖼️ **Certificate Handling**
- Template management
- Certificate designer
- Email delivery to student & admin
- Live certificate verification

📬 **Email Integration**
- SMTP with Gmail
- Sends certificate as attachment
- Verification link included

---

## 🛠 Tech Stack

| Layer        | Tech                                       |
|--------------|--------------------------------------------|
| Language     | Python 3.10                                |
| Web Framework| Flask                                      |
| Database     | SQLite (Dev), MySQL (Production)           |
| ORM          | SQLAlchemy                                 |
| Auth         | bcrypt hashing                             |
| Mail         | Flask-Mail with Gmail SMTP                 |
| Frontend     | HTML, CSS (responsive), Jinja2 templates   |
| Deployment   | PythonAnywhere                             |

---

## 🧑‍💻 Local Setup

```bash
git clone https://github.com/Tanay-Bhatt/ecertify.git
cd ecertify

# Optional virtualenv
python3 -m venv venv
source venv/bin/activate

# Set app variables in app.py , routes.py
# Set admin credentials in create_admin_user.py

python create_admin_user.py

pip install -r requirements.txt
flask run
```

## 📦 Requirements

To run E-Certify locally or on a server, make sure you have:

- Python 3.8+ (tested with 3.10)
- pip
- Git (for cloning the repo)
- Virtualenv (recommended)
- An SMTP-enabled Gmail account for email sending
- VS code or any IDE



## ⚙️ How It Works

1. **Admin Login**  
   - Admin logs into the dashboard using secure hashed credentials.

2. **Student Management**  
   - Admin can add students manually or upload a CSV file.
   - Students are saved in the database with default passwords.

3. **Template Handling**  
   - Admin uploads or selects from preloaded certificate templates.
   - Templates are previewable in the UI before use.

4. **Certificate Generation**  
   - Admin selects a student and a template.
   - A certificate is generated with the student's name and custom message.
   - Certificate is saved and emailed to the student and admin.

5. **Email Notification**  
   - Flask-Mail sends the certificate as a PNG attachment.
   - Verification link is included in the email.

6. **Verification**  
   - Anyone can verify a certificate by visiting `/verify/<certificate_id>`.

7. **Production Deployment (Optional)**  
   - App can run with MySQL and is production-ready for platforms like PythonAnywhere.