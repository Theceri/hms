from sqlalchemy.orm import backref
from main import db

class Doctor(db.Model):
    __tablename__ = 'doctors'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    designation = db.Column(db.String(80), unique=False, nullable=False)

    patients = db.relationship('Patient', backref='doctors', lazy=True)
    staff = db.relationship('Staff', backref='doctors', lazy=True)