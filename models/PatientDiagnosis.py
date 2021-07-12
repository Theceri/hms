from sqlalchemy.orm import backref
from main import db

class PatientDiagnosis(db.Model):
    __tablename__ = 'patient_diagnosis'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    diagnosis_details = db.Column(db.Text, nullable=False)
    remark = db.Column(db.Text, nullable=False)
    other = db.Column(db.Text, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())