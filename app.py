from flask import Flask, render_template, request, redirect, url_for
from flask import g
import sqlite3
import os
from flask import json
import time
from werkzeug import secure_filename

app = Flask(__name__)
DATABASE = './database.db'
UPLOAD_FOLDER = '/home/ubuntu/InvicHack/static/pic'
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods = ['GET'])	
def index():
    return render_template("index.html")

# ############### DATABASE  MODULE ##############

# connect to database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
# close database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# do some query
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# get items' infos from database
def getInfo(name):
	info = query_db('select * from items where name = ?',[name], one = True)
	if info is None:
		return "no such item"
	return info

####################################################
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
# # show info about item, 

@app.route('/show', methods = ['GET', 'POST'])
def show():
    if request.method == 'POST':
        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
                filename = '1.jpg'
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.system('python /home/ubuntu/caffe/examples/ssd/ssd_detect.py')
        data=open('/home/ubuntu/InvicHack/static/info.txt')
        datas=data.readlines()
        data.close()
        objnum=int(datas[0].strip())
        obj=[]
        namedes = []
        info = []
        for line in datas[1:]:
            line=line.split()
            obj.append([line[0],float(line[1]),float(line[2]),float(line[3]),float(line[4])])

        for o in obj:
            namedes = list(query_db('select * from items where name = ?', [o[0]], one = True))
            namedes.append(o[1])
            namedes.append(o[2])
            namedes.append(o[3])
            namedes.append(o[4])
            info.append(namedes)
        return render_template("show.html", info = info)

if __name__ == '__main__':
    app.run(debug=True)
