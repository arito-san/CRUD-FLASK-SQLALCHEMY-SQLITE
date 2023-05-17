from flask import Flask, render_template, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()
app = Flask(__name__, template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"

class Students(db.Model):
    cpf = db.Column( db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    grades_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=True)
    def __init__(self, cpf, name, birthdate, age, gender, grades_id):
        self.cpf = cpf
        self.name = name
        self.birthdate = birthdate
        self.age = age
        self.gender = gender
        self.grades_id = grades_id

class Grades(db.Model):
    id = db.Column( db.Integer, primary_key=True,autoincrement=True, nullable=False)
    av1 = db.Column(db.Float, nullable=True)
    av2 = db.Column(db.Float, nullable=True)
    average = db.Column(db.Float, nullable=True)
    students = db.relationship('Students', backref='students', uselist=False)
    def __init__(self, id, av1, av2, average, students):
        self.id = id
        self.av1 = av1
        self.av2 = av2
        self.average = average
        self.students = students

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/createStudents', methods=['POST'])
def createStudents():
    body = request.get_json()
    students = Students(cpf=body['cpf'], name= body['name'], birthdate= body['birthdate'], age= body['age'], gender= body['gender'])
    # db.session.add(students)
    # db.session.commit()
    return students

if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
        app.run(debug=True)