from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()
db = SQLAlchemy(app)
ma = Marshmallow(app)

# The above class defines a Task model with id, title, and description attributes, and an initializer
# method.
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, title, description):
        self.title = title
        self.description = description

#Lee todas las clases que sean db.Models.
#Crea todas las tablas que tengamos definidas como en este caso Task
db.create_all()

#Creamos un esquema para interactuar de forma facil con nuestros modelos.
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema  = TaskSchema(many=True)

#Definimos las rutas
@app.route('/tasks', methods=['POST'])
def create_task():
    print(request.json)

    title = request.json['title']
    description = request.json['description']

    new_task = Task(title, description)
    print("Tarea creada con éxito.")

    db.session.add(new_task)
    db.session.commit()
    print("Almacenamiento en la base de datos --> OK!")

    return jsonify(new_task)

##Ruta READ ALL - GET
@app.route('/tasks', methods=['GET'])

def get_tasks():
    all_tasks = Task.query.all()
    result = task_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/task/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.session.get(Task, id)
    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description 
    db.session.commit()


    return jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.session.get(Task, id)
    db.session.delete(task)
    db.session.commit()

    return jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'Welcome to my first API with Python Flask and MySQL'})

@app.route('/tasks/delete', methods=['DELETE'])
def delete_tasks():
    db.session.query(Task).delete()
    db.session.commit()

    return jsonify({"message":"All tasks deleted!!!"})

if __name__ == "__main__":
    app.run(debug=True)