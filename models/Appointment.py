from sqlalchemy.orm import backref
from main import db

class Appointment(db.Model):
    __tablename__ = 'appointments'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False) 