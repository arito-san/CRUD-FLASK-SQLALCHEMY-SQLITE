from flask import Flask, render_template, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

db = SQLAlchemy()
app = Flask(__name__, template_folder='static', static_folder='static', static_url_path='/')
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"

class Students(db.Model):
    cpf = db.Column( db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    grades = db.relationship('Grades', backref='students', uselist=False, )
    def to_json(self):
        return {
            "cpf":self.cpf,
            "name":self.name,
            "birthdate":self.birthdate,
            "age":self.age,
            "gender":self.gender,
            "grades":(self.grades if self.grades==None else self.grades.to_json())            
            }

class Grades(db.Model):
    id = db.Column( db.Integer, primary_key=True,autoincrement=True, nullable=False)
    av1 = db.Column(db.Float, nullable=True)
    av2 = db.Column(db.Float, nullable=True)
    average = db.Column(db.Float, nullable=True)
    students_cpf = db.Column(db.Integer, db.ForeignKey('students.cpf'), nullable=True, unique=True)
    def to_json(self):
        return {
            "id":self.id,
            "av1":self.av1,
            "av2":self.av2,
            "average":self.average,
            "students_cpf":self.students_cpf,
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/createStudents', methods=['POST'])
def createStudents():
    body = request.get_json()
    try:
        students = Students(cpf=body['cpf'], name= body['name'], birthdate= body['birthdate'], age= body['age'], gender= body['gender'], grades=body['grades'])
        db.session.add(students)
        db.session.commit()
        return response(201,"students",students.to_json(), "Criado com sucesso")
    except Exception as e:
        print(e)
        return response(400,"students",{},"Erro ao cadastrar usuário")

@app.route('/createGrades', methods=['POST'])
def createGrades():
    body = request.get_json()
    try:
        grades = Grades( av1=body['av1'], av2= body['av2'], average= body['average'], students_cpf= body['students_cpf'])
        db.session.add(grades)
        db.session.commit()
        return response(201,"grades",grades.to_json(), "Adicionada com sucesso")
    except Exception as e:
        print(e)
        return response(400,"grades",{},"Erro ao cadastrar notas")
    

@app.route('/searchStudents/<cpf>')
def searchOneStudent(cpf):
    try:
        students_obj = Students.query.filter_by(cpf=cpf).first()
        students_json = students_obj.to_json()
        return response(201,"students",students_json,'ok')
    except Exception as e:
         print(e)
         return response(400,"students",{},"Erro ao buscar estudante.")
    
@app.route('/deleteStudents/<cpf>', methods=['DELETE'])
def deleteStudent(cpf):
    students_obj = Students.query.filter_by(cpf=cpf).first()
    try:
        db.session.delete(students_obj)
        db.session.commit()
        return response(201,"students",students_obj.to_json(), "Deletado com sucesso")
    except Exception as e:
        print(e)
        return response(400,"students",{},"Erro ao deletar")
@app.route('/updateStudents/<cpf>', methods=['PUT'])
def updateStudent(cpf):
       students_obj = Students.query.filter_by(cpf=cpf).first()
       body = request.get_json()
       try:
            if('name' in body):
                students_obj.name=body['name']
            db.session.add(students_obj)
            db.session.commit()
            return response(201,"students",students_obj.to_json(), "Atualizado com sucesso")
       except Exception as e:
            return response(400,"students",{},"Erro ao atualizar")
       
@app.route('/searchAllStudents', methods=['GET'])
def allStudents():
    students_obj = Students.query.all()
    students_json = [students.to_json() for students in students_obj]
    return response(201,"students",students_json, "Todos os usuários cadastrado.")

def response(status,contentName, content, message=False):
    body = {}
    body[contentName] = content
    if(message):
        body["message"]=message
    return Response(json.dumps(body), status=status, mimetype="application/json")

if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
        app.run(debug=True)