from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Init app
app = Flask(__name__)

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:'superone@321'@localhost/flask_app_db1"
db = SQLAlchemy(app)

# creating database schema
class Student(db.Model):
    __tablename__='students'
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(40))
    lname=db.Column(db.String(40))
    dept=db.Column(db.String(40))

    def __init__(self,fname,lname,dept):
        self.fname=fname
        self.lname=lname
        self.dept=dept


@app.route('/add_student')
def add_student():
    fname = request.json['fname']
    lname = request.json['lname']
    dept = request.json['dept']

    student=Student(fname,lname,dept)
    db.session.add(student)
    db.session.commit()
    return jsonify({"msg":"student added"})

@app.route('/get_student_list')
def all_student():
    return jsonify({"msg":"student list"})

@app.route('/get_indivisual_student/<id>')
def indivisual_student(id):
    print(id)
    return jsonify({"msg":"indivisual student record"})

@app.route('/update_student/<id>')
def update_student(id):
    print(id)
    return jsonify({"msg":"student updated"})

@app.route('/delete_student/<id>')
def delete_student(id):
    print(id)
    return jsonify({"msg":"student deleted!"})


# Run Server
if __name__ == '__main__':
    # do not use debug = True in production server
    app.run(debug=True)