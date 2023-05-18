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

    def to_json(self):
        return {
            "cpf":self.cpf,
            "name":self.name,
            "birthdate":self.birthdate,
            "age":self.age,
            "gender":self.gender,
            "grades_id":self.grades_id            
            }

class Grades(db.Model):
    id = db.Column( db.Integer, primary_key=True,autoincrement=True, nullable=False)
    av1 = db.Column(db.Float, nullable=True)
    av2 = db.Column(db.Float, nullable=True)
    average = db.Column(db.Float, nullable=True)
    students = db.relationship('Students', backref='students', uselist=False)
    def to_json(self):
        return {
            "id":self.id,
            "av1":self.av1,
            "av2":self.av2,
            "average":self.average,
            "students":self.students,
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/createStudents', methods=['POST'])
def createStudents():
    body = request.get_json()
    try:
        students = Students(cpf=body['cpf'], name= body['name'], birthdate= body['birthdate'], age= body['age'], gender= body['gender'], grades_id=body['grades_id'])
        db.session.add(students)
        db.session.commit()
        return response(201,"students",students.to_json(), "Criado com sucesso")
    except Exception as e:
        print(e)
        return response(400,"students",{},"Erro ao cadastrar usuário")
def response(status,contentName, content, mensagem=False):
    body = {}
    body[contentName] = content
    if(mensagem):
        body["mensagem"]=mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")

@app.route('/searchStudents/<cpf>')
def searchOneStudent(cpf):
    students_obj = Students.query.filter_by(cpf=cpf).first()
    students_json = students_obj.to_json()
    return response(201,"students",students_json)

if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
        app.run(debug=True)