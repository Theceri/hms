from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

app = Flask(__name__)

db = SQLAlchemy(app)

from configs.base_config import *

app.config.from_object(Development)

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

if __name__ == '__main__':
    app.run()