from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

app = Flask(__name__)

ma = Marshmallow(app)

from configs.base_config import *
app.config.from_object(Development)

db = SQLAlchemy(app)

from models.Patient import Patient
from models.Doctor import Doctor
from models.Staff import Staff
from models.Bill import Bill
from models.Appointment import Appointment
from models.Role import Role

@app.before_first_request
def create_tables():
    db.create_all()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized! Please log in', 'danger')
            return redirect(url_for('login', next = request.url))
    return wrap

@app.route('/', methods = ['GET', 'POST'])
@login_required
def dashboard():

    return render_template('dashboard.html')

@app.route('/patients', methods = ['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
    roles = Role.query.all()
    medical_staff = Staff.query.all()

    return render_template('doctors.html', genders = genders, medical_staff = medical_staff, roles = roles)

@app.route('/edit_doctor', methods = ['POST'])
@login_required
def edit_doctor():
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        telephone = request.form['telephone']

        staff_to_edit = Staff.query.filter_by(id = doctor_id).first()
        staff_to_edit.first_name = first_name
        staff_to_edit.last_name = last_name
        staff_to_edit.department = department
        staff_to_edit.telephone = telephone

        db.session.add(staff_to_edit)
        db.session.commit()

        flash("Doctor data successfully edited", "success")

        return redirect(url_for('doctors'))

@app.route('/staff', methods = ['GET', 'POST'])
@login_required
def staff():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        role = request.form['role']
        telephone = request.form['telephone']
        email = request.form['email']
        password =  request.form['password']
        hashed_password = generate_password_hash(password = password)

        # check that email does not exist before registering the user
        if Staff.check_email_exists(email):
            flash("The user already exists. Please try registering with a different email.", "danger")
        else:
            new_staff_member = Staff(first_name = first_name, last_name = last_name, department = department, role = role, telephone = telephone, email = email, password = hashed_password)

            db.session.add(new_staff_member)
            db.session.commit()

            flash("Staff member successfully registered", "success")
        
    genders = ['M', 'F']
    staff = Staff.query.all()
    roles = Role.query.all()

    return render_template('staff.html', genders = genders, staff = staff, roles = roles)

@app.route('/edit_staff', methods = ['POST'])
@login_required
def edit_staff():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        role = request.form['role']
        telephone = request.form['telephone']
        
        staff_to_edit = Staff.query.filter_by(id = staff_id).first()
        staff_to_edit.first_name = first_name
        staff_to_edit.last_name = last_name
        staff_to_edit.department = department
        staff_to_edit.role = role
        staff_to_edit.telephone = telephone

        db.session.add(staff_to_edit)
        db.session.commit()

        flash("Staff data successfully edited", "success")

        return redirect(url_for('staff'))

@app.route('/dashboard_doc', methods = ['POST'])
@login_required
def dashboard_doc():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    department = request.form['department']
    role = request.form['role']
    telephone = request.form['telephone']
    email = request.form['email']
    password =  '1234'
    hashed_password = generate_password_hash(password = password)

    # check that email does not exist before registering the user
    if Staff.check_email_exists(email):
        flash("The user already exists. Please try registering with a different email.", "danger")
    else:
        new_staff_member = Staff(first_name = first_name, last_name = last_name, department = department, role = role, telephone = telephone, email = email, password = hashed_password)

        db.session.add(new_staff_member)
        db.session.commit()

        flash("Doctor successfully registered", "success")

    return redirect(url_for('doctors'))

@app.route('/appointments', methods = ['GET', 'POST'])
@login_required
def appointments():
    if request.method == 'POST':
        patient = request.form['patient']
        doctor = request.form['doctor']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        triage_report = request.form['triage_report']
        symptoms_report = request.form['symptoms_report']
        medication_report = request.form['medication_report']
        other_remarks = request.form['other_remarks']
        lab_report = request.form['lab_report']

        new_appointment = Appointment(patient = patient, doctor = doctor, start_time = start_time, end_time = end_time, triage_report = triage_report, symptoms_report = symptoms_report, medication_report = medication_report, other_remarks = other_remarks, lab_report = lab_report)

        db.session.add(new_appointment)
        db.session.commit()

        flash("Appointment successfully created", "success")

    patients = Patient.query.all()
    doctors = Doctor.query.all()
    appointments = Appointment.query.all()

    return render_template('appointments.html', patients = patients, doctors = doctors, appointments = appointments)

@app.route('/edit_appointment', methods = ['POST'])
@login_required
def edit_appointment():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        patient = request.form['patient']
        doctor = request.form['doctor']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        triage_report = request.form['triage_report']
        symptoms_report = request.form['symptoms_report']
        medication_report = request.form['medication_report']
        other_remarks = request.form['other_remarks']
        lab_report = request.form['lab_report']
        
        print(triage_report)
        print(symptoms_report)
        print(medication_report)
        print(other_remarks)
        print(lab_report)

        appointment_to_edit = Appointment.query.filter_by(id = appointment_id).first()
        appointment_to_edit.patient_id = patient
        appointment_to_edit.doctor_id = doctor
        appointment_to_edit.start_time = start_time
        appointment_to_edit.end_time = end_time
        appointment_to_edit.triage_report = triage_report
        appointment_to_edit.symptoms_report = symptoms_report
        appointment_to_edit.medication_report = medication_report
        appointment_to_edit.other_remarks = other_remarks
        appointment_to_edit.lab_report = lab_report

        db.session.add(appointment_to_edit)
        db.session.commit()

        flash("Appointment data successfully edited", "success")

        return redirect(url_for('appointments'))

@app.route('/appointments/<int:x>', methods = ['GET'])
def patient_appointments(x):
    if request.method == 'GET':
        patient_appointments = Appointment.query.filter_by(patient = x).all()
        print(patient_appointments)

        return render_template('appointments.html', appointments = patient_appointments)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        role = request.form['role']
        telephone = request.form['telephone']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password = password)

        # check that email does not exist before registering the user
        if Staff.check_email_exists(email):
            flash("The user already exists. Please try registering with a different email.", "danger")
        else:
            new_staff_member = Staff(first_name = first_name, last_name = last_name, department = department, role = role, telephone = telephone, email = email, password = hashed_password)

            db.session.add(new_staff_member)
            db.session.commit()

            flash("You have successfully signed up. You can now log in to your account.", "success")

            return redirect(url_for('login'))

    genders = ['M', 'F']
    roles = Role.query.all()

    return render_template('register.html', genders = genders, roles = roles)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # check if email exist
        if Staff.check_email_exists(email = email):
           # if the email exists check if password is correct
           if Staff.check_password(email = email, password = password):
               session['logged_in'] = True
               session['first_name'] = Staff.fetch_by_email(email).first_name

               return redirect(url_for('dashboard'))
           else:
               flash("Incorrect password","danger")

               return render_template('login.html')
        else:
            flash("Email does not exist","danger")

    return render_template("login.html")

# Log Out route
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')

    return redirect(url_for('login'))

@app.route('/roles', methods = ['GET', 'POST'])
@login_required
def roles():
    if request.method == 'POST':
        name = request.form['name']

        new_role = Role(name = name)

        db.session.add(new_role)
        db.session.commit()

        flash("Role successfully added", "success")
        
    roles = Role.query.all()

    return render_template('roles.html', roles = roles)

@app.route('/edit_role', methods = ['POST'])
@login_required
def edit_role():
    if request.method == 'POST':
        role_id = request.form['role_id']
        name = request.form['name']

        role_to_edit = Role.query.filter_by(id = role_id).first()
        role_to_edit.name = name

        db.session.add(role_to_edit)
        db.session.commit()

        flash("Role data successfully edited", "success")

        return redirect(url_for('roles'))

if __name__ == '__main__':
    app.run()