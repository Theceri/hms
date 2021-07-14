from sqlalchemy.orm import backref
from main import db

class Staff(db.Model):
    __tablename__ = 'staff'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    department = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    telephone = db.Column(db.String(80), unique=False, nullable=False)