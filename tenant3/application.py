import json
from flask import Flask, render_template, request, session, flash, redirect, jsonify, json, Response
import zipfile
from flask_cors import CORS
from werkzeug import secure_filename
import os
import subprocess
from subprocess import *
import base64
from flask import send_file


application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = 'uploads/'


CORS(application)


@application.route("/tenant3", methods=['POST'])
def upload():
    #Code to upload file
    file = request.files['file']
    filename = secure_filename(file.filename)
    print(filename)
    file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
    
    generateUML(application.config['UPLOAD_FOLDER'] + filename)
    return getImage()

def generateUML(inputfilepath):
    print("generateUML")
    #extract file and do stuff
    
    args= ["java", "-jar", "parser.jar" ,inputfilepath,"output"]
    application.config['OUTPUT_FOLDER'] = 'uploads/out/'
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    result = popen.stdout.read()
    print(result)
    

def clean_dir():
    print("Cleaning Uploaded Directory")
    import os, shutil
    for the_file in os.listdir(application.config['uploads/out/']):
        file_path = os.path.join(application.config['uploads/out/'], the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
            

def getImage():
    print("return image")
    with open(application.config['OUTPUT_FOLDER'] + "/output.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('UTF-8')
        resp = jsonify({"result": encoded_string})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        #clean_dir()
        return resp

if __name__ == "__main__":
    print("running on 0.0.0.0")
    application.run(host='0.0.0.0')
        
