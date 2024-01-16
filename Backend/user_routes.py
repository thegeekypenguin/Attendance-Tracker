#Here we will deal with user profiles mostly

from __main__ import app, mongo
import os
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from face_detector import faceEncodings

# allowed images extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# here we are registering new users
@app.route('/api/user',methods=['POST'])
def add_user():
    user_name=request.form['name']
    email=request.form['email']
    password=request.form['password']

    #check if file is present
    if 'photo' not in request.files:
        return jsonify({'success':False,'message':"please upload your recent photo"})

    profile_picture=request.files['photo']
    #check if file is actually an image
    if not profile_picture or not allowed_file(profile_picture.filename):
        return jsonify({'success':False,'message':'only images are allowed (jpg, jpeg, png)'}).status_code(400)
    if (request.method!='POST') or (not user_name) or (not password) or (not email) or (not profile_picture):
        return jsonify({'success':False,'message':"Complete all the fields"}).status_code(400)

    #check if email is already registered
    check = mongo.db.users.find_one({'email':email})
    if check:
        response = jsonify({'success':False,'message':"email already registered"})
        response.status_code=400
        return response

    hashed_password = generate_password_hash(password)

    #saving file to local database
    filename=secure_filename(email+'.'+profile_picture.filename.rsplit('.', 1)[1].lower())
    profile_picture.save(os.path.join(app.config['UPLOAD-FOLDER'],filename))
    
    isEncoded=faceEncodings(email,filename)     #saving picture's encoding to cloud database
    if not isEncoded:
        return jsonify({'success':False,'message':"Face not detected in image"})
    
    mongo.save_file(email,profile_picture) #saving image to cloud 
    try:
        id=mongo.db.users.insert_one({'name':user_name,'email':email,'password':hashed_password,'attendance':{}})
    except Exception:
        return jsonify({'success':False,'message':"account not created\nPlease try again.."}).status_code(404)
    print(id)
    response = jsonify({'success':True,'message':'New user added successfully','id':str(id)})
    return response
    
# to get a user by id
@app.route('/api/user/<userId>')
def get_profile(userId):
    user = mongo.db.users.find_one_or_404({'_id':ObjectId(userId)})
    return jsonify({'name':user['name'],'email':user['email'],'attendance':user['attendance']})

#update any user's profile
@app.route('/api/user',methods=['PUT'])
def update_profile():
    data=request.json
    _id=data['_id']
    user_name=data['name']
    email=data['email']
    password=data['password']
    
    if request.method!='PUT' or not _id or not user_name or not email or not password:
        response = jsonify({'success':False,'message':"update failed"})
        response.status_code=500
        return response
    hashed_password= generate_password_hash(password)
    mongo.db.users.update_one({'_id':ObjectId(_id)}, {'$set': {'name': user_name, 'email': email, 'password': hashed_password}})
    response=jsonify({'success':True,'message':'user updated successfully'})
    return response

# to remove a user from database
@app.route('/api/user/<userId>',methods=['DELETE'])
def remove_user(userId):
    mongo.db.users.delete_one({'_id':ObjectId(userId)})
    return jsonify({'success':True,'message':"user deleted successfully"})

#to get a list of all users (sending only email and names)
@app.route('/api/users')
def get_users():
    users=mongo.db.users.find()
    response=[]
    for user in users:
        data={}
        data['name']=user['name']
        data['email']=user['email']
        response.append(data)
    return jsonify(response)