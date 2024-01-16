# here we will manage attendance of all the people
from __main__ import app, mongo
from datetime import datetime

from bson import ObjectId
from flask import jsonify

@app.route('/api/mark/<userId>')
def mark_present(userId):
    user = mongo.db.users.find_one_or_404({'_id':ObjectId(userId)})
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    attendance = user['attendance']
    try:
        values = attendance[f'{currentMonth} {currentYear}']
    except KeyError:
        values = attendance[f'{currentMonth} {currentYear}'] = []
    for dates in values:
        if dates==currentDay:
            return jsonify({'success':True,'message':'attendance already marked'})
    values.append(currentDay)
    mongo.db.users.update_one({'_id':ObjectId(userId)}, {'$set': {'attendance':attendance}})
    return jsonify({'success':True,'message':'attendance marked successfully'})

@app.route('/api/get-attendance/<userId>')
def get_attendance(userId):
    user=mongo.db.users.find_one_or_404({'_id':ObjectId(userId)})
    attendance=user['attendance']
    return attendance    
