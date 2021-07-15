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
    doctors = Doctor.query.all()

    return render_template('doctors.html', genders = genders, doctors = doctors)

@app.route('/edit_doctor', methods = ['POST'])
@login_required
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
@login_required
def staff():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        gender = request.form['gender']
        address = request.form['address']
        telephone = request.form['telephone']
        email = request.form['email']
        password = '1234'
        hashed_password = generate_password_hash(password = password)

        # check that email does not exist before registering the user
        if Staff.check_email_exists(email):
            flash("The user already exists. Please try registering with a different email.", "danger")
        else:
            new_staff_member = Staff(first_name = first_name, last_name = last_name, department = department, gender = gender, address = address, telephone = telephone, email = email, password = hashed_password)

            db.session.add(new_staff_member)
            db.session.commit()

            flash("Staff member successfully registered", "success")
        
    genders = ['M', 'F']
    staff = Staff.query.all()

    return render_template('staff.html', genders = genders, staff = staff)

@app.route('/edit_staff', methods = ['POST'])
@login_required
def edit_staff():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        gender = request.form['gender']
        address = request.form['address']
        telephone = request.form['telephone']
        email = request.form['email']
        
        staff_to_edit = Staff.query.filter_by(id = staff_id).first()
        staff_to_edit.first_name = first_name
        staff_to_edit.last_name = last_name
        staff_to_edit.department = department
        staff_to_edit.gender = gender
        staff_to_edit.address = address
        staff_to_edit.telephone = telephone
        staff_to_edit.email = email

        db.session.add(staff_to_edit)
        db.session.commit()

        flash("Staff data successfully edited", "success")

        return redirect(url_for('staff'))

@app.route('/appointments', methods = ['GET', 'POST'])
@login_required
def appointments():
    return render_template('appointments.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        gender = request.form['gender']
        address = request.form['address']
        telephone = request.form['telephone']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password = password)

        # check that email does not exist before registering the user
        if Staff.check_email_exists(email):
            flash("The user already exists. Please try registering with a different email.", "danger")
        else:
            new_staff_member = Staff(first_name = first_name, last_name = last_name, department = department, gender = gender, address = address, telephone = telephone, email = email, password = hashed_password)

            db.session.add(new_staff_member)
            db.session.commit()

            flash("You have successfully signed up. You can now log in to your account by going to the login page.", "success")

    genders = ['M', 'F']

    return render_template('register.html', genders = genders)

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

if __name__ == '__main__':
    app.run()