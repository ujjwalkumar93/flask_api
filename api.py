from crypt import methods
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
from flask_marshmallow import Marshmallow 
# Init app
app = Flask(__name__)
# init ma
ma = Marshmallow(app)
# connect to database
password = urllib.parse.quote("superone@321")

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:ukumar@localhost/flask_db"
db = SQLAlchemy(app)

# creating database schema
class Student(db.Model):
    # here db.String(40) is nothing but the data type would be string and maximum length of that string would be 40
    #__tablename__='students'
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(40))
    lname=db.Column(db.String(40))
    dept=db.Column(db.String(40))

    def __init__(self,fname,lname,dept):
        self.fname=fname
        self.lname=lname
        self.dept=dept

class StudentSchema(ma.Schema):
  class Meta:
    fields = ('fname', 'lname', 'dept')

# Init schema to return serialize data
student_schema = StudentSchema()

@app.route('/add_student')
def add_student():
    fname = request.json['fname']
    lname = request.json['lname']
    dept = request.json['dept']
    student=Student(fname,lname,dept)
    db.session.add(student)
    db.session.commit()
    return student_schema.jsonify(student)    

@app.route('/get_student_list')
def all_student():
    all_students = Student.query.all()
    result = student_schema.dump(all_students)
    return jsonify(result)

@app.route('/get_indivisual_student/<id>')
def indivisual_student(id):
    # here id is used to fetch the record of indivisual studen
    student = Student.query.get(id)
    return student_schema.jsonify(student[0])

@app.route('/update_student/<id>',methods=["PUT"])
def update_student(id):
    student = Student.query.get(id)

    fname = request.json['fname']
    lname = request.json['lname']
    dept = request.json['dept']
    
    student.fname = fname
    student.lname = lname
    student.dept = dept
    db.session.commit()
    return student_schema.jsonify(student)

@app.route('/delete_student/<id>',methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return student_schema.jsonify(student)


# Run Server
if __name__ == '__main__':
    # do not use debug = True in production server
    app.run(debug=True)