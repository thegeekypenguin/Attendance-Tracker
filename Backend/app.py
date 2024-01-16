import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv()

UPLOAD_FOLDER = './Images'

app=Flask(__name__)
app.config["MONGO_URI"]=os.getenv('MONGO_URI')
app.config['UPLOAD-FOLDER']=UPLOAD_FOLDER
try:
    mongo = PyMongo(app)
except Exception:
    print("Can't connect to database. Check your connection..")
    quit()

CORS(app, support_credentials=True)         #to avoid CORS errors..

@app.route('/')
def hello():
    return "<h1>server is up and running...</h1>"

import user_routes
import face_detector
import attendance_manager

# error handlers
@app.errorhandler(500)
def some_error_occured(error=None):
    response=jsonify({'success':False,'message':'some error occured'})
    response.status_code=500
    return response

@app.errorhandler(404)
def not_found(error=None):
    response=jsonify({'success':False,'message':"Not found"})
    response.status_code(404)
    return response

@app.errorhandler(400)
def bad_request(error=None):
    response=jsonify({'success':False,'message':"Bad request"})
    response.status_code(400)
    return response

if __name__=='__main__':
    app.run(debug=True)