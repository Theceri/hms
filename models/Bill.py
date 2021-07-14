from sqlalchemy.orm import backref
from main import db

class Bill(db.Model):
    __tablename__ = 'bills'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    amount = db.Column(db.Integer)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))