#!/usr/bin/python
from datetime import datetime
from flask import Flask, flash, render_template, request, redirect
import MySQLdb as mdb
import json

app = Flask(__name__)
app.secret_key = 'instagram-screen-scraper'

def getUnannotatedComment():
    try:
        con = mdb.connect('localhost', 'root', 'root', 'instagram')
        con.set_character_set('utf8')
        cur = con.cursor()
        query = "SELECT * from comments where label is not null"
        cur.execute(query)
        return cur.fetchone()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        con.close()

def insertComment(data):
    try:
        con = mdb.connect('localhost', 'root', 'root', 'instagram')
        con.set_character_set('utf8')
        cur = con.cursor()
        cur.execute("INSERT INTO comments(`id`,`username`,`time`,`text`) values(%s,%s,%s,%s)", (data['id'], data['username'], datetime.fromtimestamp(data['time'] / 1e3), data['text']))
        con.commit()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        con.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.form['id'] or not request.form['spam']:
            flash('Make sure that every field has been filled!', 'error')
        else:
            flash('Label saved', 'info')
            return redirect('/')
    data = getUnannotatedComment()
    # data = {'text': 'Oh ya ya ya', 'id': '123456'}
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # filename = 'inijedar_BKnxd0rhHJz.json'
    # f = open('/home/aliakbars/Dropbox/Spam/comments/{}'.format(filename))
    # data = json.loads(f.read().strip())
    # insertComment(data[0])