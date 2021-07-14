from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

app = Flask(__name__)

from configs.base_config import *
app.config.from_object(Development)

db = SQLAlchemy(app)

from models.Patient import Patient
from models.Doctor import Doctor
from models.Staff import Staff
from models.PatientDiagnosis import PatientDiagnosis
from models.Bill import Bill

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods = ['GET', 'POST'])
def dashboard():
    # orgs = Org.query.all()
    # branches = Branch.query.all()
    # users = User.query.all()
    # surveys = Survey.query.all()
    # questions = Question.query.all()
    # respondents = Respondent.query.all()
    # answers = Answer.query.all()
    # number_of_respondents = Respondent.query.count()

    return render_template('dashboard.html')

@app.route('/patients', methods = ['GET', 'POST'])
def patients():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        address = request.form['address']
        telephone = request.form['telephone_number']
        doctor = request.form['doctor']

        new_patient = Patient(first_name = first_name, last_name = last_name, gender = gender, address = address, telephone = telephone, doctor_id = doctor)

        db.session.add(new_patient)
        db.session.commit()

        flash("Patient successfully added", "success")

    genders = ['M', 'F']
    patients = Patient.query.all()
    doctors = Doctor.query.all()    

    return render_template('patients.html', genders = genders, patients = patients, doctors = doctors)

@app.route('/doctors', methods = ['GET', 'POST'])
def doctors():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        address = request.form['address']
        designation = request.form['designation']

        new_doctor = Doctor(first_name = first_name, last_name = last_name, gender = gender, address = address, designation = designation)

        db.session.add(new_doctor)
        db.session.commit()

        flash("Doctor successfully added", "success")
        
    genders = ['M', 'F']
    doctors = Doctor.query.all()

    return render_template('doctors.html', genders = genders, doctors = doctors)

@app.route('/staff', methods = ['GET', 'POST'])
def staff():
    return render_template('staff.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    pass

if __name__ == '__main__':
    app.run()