from app import db
from admin.models import CertifyUser
from scripts.password import hash_password
from datetime import datetime

existing = CertifyUser.query.filter_by(username="{adminusername}").first()
if existing:
    print("⚠️ Admin user already exists.")
else:
    register = CertifyUser(
        username="{adminusername}",
        name="{adminusername}",
        password=hash_password("{adminupassword}"),
        email="{adminmail}",
        phone_num="{adminnumber}",
        date_added=datetime.now(),
        role="admin"
    )
    db.session.add(register)
    db.session.commit()
    print("✅ Admin user created successfully.")