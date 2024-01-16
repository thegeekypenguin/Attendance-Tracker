#here we will add some logic for detecting face

from __main__ import app,mongo
from flask import jsonify, redirect
import cv2
from bson.binary import Binary
import pickle
import numpy as np
import face_recognition

#encoding via HOG algorithm
def faceEncodings(email,filename):
    img=cv2.imread(f'Images/{filename}')
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    try:
        encode = face_recognition.face_encodings(img)[0]
    except IndexError:         
        return False
    mongo.db.encodings.insert_one({"person":email,"encoding":Binary(pickle.dumps(encode, protocol=2), subtype=128 )})
    return True

@app.route('/api/mark-my-attendance')
def detectMe():
    current_person="unknown"
    try:
        temp=mongo.db.encodings.find()
    except Exception:
        return jsonify({'success':False,'message':"Some error occured..."})
    encodeListKnown=[]
    person=[]
    for item in temp:
        encodeListKnown.append(pickle.loads(item['encoding']))
        person.append(item['person'])

    cap = cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        faces = cv2.resize(frame,(0,0),None,0.25,0.25)
        faces=cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)
        facesCurrentFrame=face_recognition.face_locations(faces)
        encodesCurrentFrame= face_recognition.face_encodings(faces,facesCurrentFrame)

        for encodeFace,faceLoc in zip(encodesCurrentFrame,facesCurrentFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            matchIndex=np.argmin(faceDis)
            if matches[matchIndex]:
                user=mongo.db.users.find_one_or_404({'email':person[matchIndex]})
                name=user['name']
                current_person = user['_id']
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.75,(0,0,255),2)
        
        cv2.imshow("WebCam",frame)
        cv2.setWindowProperty("WebCam", cv2.WND_PROP_TOPMOST, 1)
        cv2.setWindowProperty("WebCam",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty("WebCam",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)
        if cv2.waitKey(100)==13:
            break
    cap.release()
    cv2.destroyAllWindows()
    if current_person != "unknown":
        return redirect(f'http://localhost:5000/api/mark/{current_person}')
    return jsonify({"succes":False,"message":"no match found"})