from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import mqtt, socketio

main = Blueprint('main', __name__)

actuator = 0
logged_in_students = {}

@main.route("/")  
def index():
    return redirect(url_for('home'))

@main.route("/home")
def home():
    stu_number = request.cookies.get('stu_number')
    if stu_number in logged_in_students.keys():
        return render_template("index.html", is_logged_in=True)
    else:
        return render_template("index.html", is_logged_in=False)

@main.route('/graph')
def graph():
    return render_template("graph.html")

@main.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        stu_number = request.form['stu_number']
        if ("fct.unl.pt" in email) and (stu_number not in logged_in_students.keys()):
            response = jsonify({"success":True})
            response.set_cookie('email', email, max_age=60*60*24*2)
            response.set_cookie('stu_number', stu_number, max_age=60*60*24*2)
            logged_in_students[stu_number] = email
        else:
            response = jsonify({"success":False})
        return response
    #return render_template("login.html")

@main.route("/logout", methods=['POST'])
def logout():
    logged_in_students.pop(request.cookies.get("stu_number"))
    return render_template("index.html")

@main.route('/get_table')
def get_table():
    print(logged_in_students)
    return jsonify(logged_in_students)

@main.route("/upload")
def upload():
    return render_template("upload.html")

@main.route('/data', methods = ['GET'])
def data():
    return jsonify(result=random.randint(0,10)) 

@main.route('/button_test_page')
def button_test_page():
    return render_template("button_test.html")