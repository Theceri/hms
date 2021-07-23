from sqlalchemy.orm import backref
from main import db

class Patient(db.Model):
    __tablename__ = 'patients'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    telephone = db.Column(db.String(80), unique=False, nullable=False)
    # doctor = db.Column(db.Integer, db.ForeignKey('staff.id'))
    
    bill = db.relationship('Bill', backref='patients', lazy=True)
    appointments = db.relationship('Appointment', backref='patients', lazy=True)