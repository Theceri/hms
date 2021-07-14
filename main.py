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
from models.Appointment import Appointment

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

@app.route('/edit_patient', methods = ['POST'])
def edit_patient():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        address = request.form['address']
        telephone = request.form['telephone']
        doctor = request.form['doctor']

        patient_to_edit = Patient.query.filter_by(id = patient_id).first()
        patient_to_edit.first_name = first_name
        patient_to_edit.last_name = last_name
        patient_to_edit.gender = gender
        patient_to_edit.address = address
        patient_to_edit.telephone = telephone
        patient_to_edit.doctor_id = doctor

        db.session.add(patient_to_edit)
        db.session.commit()

        flash("Patient data successfully edited", "success")

        return redirect(url_for('patients'))

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

@app.route('/edit_doctor', methods = ['POST'])
def edit_doctor():
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        address = request.form['address']
        designation = request.form['designation']

        doctor_to_edit = Doctor.query.filter_by(id = doctor_id).first()
        doctor_to_edit.first_name = first_name
        doctor_to_edit.last_name = last_name
        doctor_to_edit.gender = gender
        doctor_to_edit.address = address
        doctor_to_edit.designation = designation

        db.session.add(doctor_to_edit)
        db.session.commit()

        flash("Doctor data successfully edited", "success")

        return redirect(url_for('doctors'))

@app.route('/staff', methods = ['GET', 'POST'])
def staff():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        gender = request.form['gender']
        address = request.form['address']
        telephone = request.form['telephone']

        new_staff = Staff(first_name = first_name, last_name = last_name, department = department, gender = gender, address = address, telephone = telephone)

        db.session.add(new_staff)
        db.session.commit()

        flash("Staff member successfully registered", "success")
        
    genders = ['M', 'F']
    staff = Staff.query.all()

    return render_template('staff.html', genders = genders, staff = staff)

@app.route('/edit_staff', methods = ['POST'])
def edit_staff():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        gender = request.form['gender']
        address = request.form['address']
        telephone = request.form['telephone']
        
        staff_to_edit = Staff.query.filter_by(id = staff_id).first()
        staff_to_edit.first_name = first_name
        staff_to_edit.last_name = last_name
        staff_to_edit.department = department
        staff_to_edit.gender = gender
        staff_to_edit.address = address
        staff_to_edit.telephone = telephone

        db.session.add(staff_to_edit)
        db.session.commit()

        flash("Staff data successfully edited", "success")

        return redirect(url_for('staff'))

@app.route('/appointments', methods = ['GET', 'POST'])
def appointments():
    return render_template('appointments.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    pass

if __name__ == '__main__':
    app.run()