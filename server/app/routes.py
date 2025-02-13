from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os

logged_in_students = {}

ALLOWED_EXTENSIONS = {'py', 'txt'}

def register_routes(app):

    @app.route("/")  
    def index():
        return redirect(url_for('home'))

    @app.route("/home")
    def home():
        stu_number = request.cookies.get('stu_number')
        if stu_number in logged_in_students.keys():
            return render_template("index.html", is_logged_in=True)
        else:
            return render_template("index.html", is_logged_in=False)

    @app.route('/graph')
    def graph():
        return render_template("graph.html")

    @app.route("/login", methods=['POST'])
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

    @app.route("/logout", methods=['POST'])
    def logout():
        logged_in_students.pop(request.cookies.get("stu_number"))
        return render_template("index.html")

    @app.route('/get_table')
    def get_table():
        print(logged_in_students)
        return jsonify(logged_in_students)

    @app.route('/get_auth_state')
    def get_auth_state():
        stu_number = request.cookies.get('stu_number')
        is_logged_in = stu_number in logged_in_students.keys()
        return jsonify({"is_logged_in": is_logged_in})

    @app.route("/upload")
    def upload():
        return render_template("upload.html")

    @app.route('/data', methods = ['GET'])
    def data():
        return jsonify(result=random.randint(0,10)) 

    def allowed_file(filename):
        return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/upload_file/<stu_number>', methods=['POST'])
    def upload_file(stu_number):
        if 'file' not in request.files:
            return jsonify({'success': False, 'message':'No file found'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success':False, 'message':'No file selected'}), 400
        if file.filename != str(stu_number):
            return jsonify({'success':False, 'message':'filename different from student number'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            stu_dir = os.path.join(app.config['UPLOAD_FOLDER'],stu_number)
            os.makedirs(stu_dir, exist_ok=True)
            file_path = os.path.join(stu_dir, filename)
            file.save(file_path)
            return jsonify({'success':True, 'message':'File upload success','filename':filename}), 200
        return jsonify({'success':False, 'message':'File type not allowed'})
    
    @app.route('/upload_text/<stu_number>', methods=['POST'])
    def upload_text(stu_number):
        print(stu_number)
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'success':False, 'message': 'Text was empty'}), 400
        stu_dir = os.path.join(app.config['UPLOAD_FOLDER'],stu_number)
        os.makedirs(stu_dir, exist_ok=True)
        file_path = os.path.join(stu_dir, str(stu_number)+'.py')
        print(file_path)
        with open(file_path,'w') as f:
            f.write(text)
            f.close()
        return jsonify({'success': True, 'message':'saved'}), 200

    @app.route('/mqtt_test', methods=['POST'])
    def mqtt_test():
        global actuator
        actuator = request.form['message']
        (result, mid) = mqtt.publish('home/actuator', int(actuator).to_bytes(1,'big'))
        if(result == mqtt_client.MQTT_ERR_SUCCESS):
            print("MQTT message success - " + actuator)
        else:
            print("MQTT message failed. Error: " + result)
        return redirect(url_for('graph'))