#!/usr/bin/python
from datetime import datetime
from flask import Flask, flash, render_template, request, redirect
import json
import psycopg2
import os
import random

app = Flask(__name__)
app.secret_key = 'instagram-screen-scraper'

file_in_dir = 'data/comments/'
file_out_dir = 'data/label/'
posts_dir = 'data/posts_160923/'

def getUnannotatedComment():
    try:
        con = psycopg2.connect(host=os.ENVIRON['PSQL_HOST'], user=os.ENVIRON['PSQL_USER'], password=os.ENVIRON['PSQL_PASS'], dbname=os.ENVIRON['PSQL_INSTA'])
        cur = con.cursor()
        query = "SELECT * from comments where label is not null offset random() * (select count(*) from comments) limit 1"
        cur.execute(query)
        return cur.fetchone()
    except psycopg2.Error as e:
        print e.pgerror
    finally:
        con.close()

def insertComment(data, filename):
    try:
        con = psycopg2.connect(host=os.environ['PSQL_HOST'], user=os.environ['PSQL_USER'], password=os.environ['PSQL_PASS'], dbname=os.environ['PSQL_INSTA'])
        cur = con.cursor()
        cur.execute("INSERT INTO comments(id,username,time,text,filename) values(%s,%s,%s,%s,%s)", (data['id'], data['username'], datetime.fromtimestamp(data['time'] / 1e3), data['text'], filename,))
        con.commit()
    except psycopg2.Error as e:
        print e.pgerror
    finally:
        con.close()

def updateLabel(comment_id, label):
    try:
        con = psycopg2.connect(host=os.environ['PSQL_HOST'], user=os.environ['PSQL_USER'], password=os.environ['PSQL_PASS'], dbname=os.environ['PSQL_INSTA'])
        cur = con.cursor()
        cur.execute("UPDATE comments SET label=%s WHERE id=%s", (label, comment_id,))
        con.commit()
    except psycopg2.Error as e:
        print e.pgerror
    finally:
        con.close()

def getComments():
    file_in = os.listdir(file_in_dir)
    file_out = os.listdir(file_out_dir)
    f = random.sample(set(file_in) - set(file_out), 1)[0]
    return json.loads(open(file_in_dir + f).read())[:50], f

def getPost(username, post_id):
    with open(posts_dir + '{}.json'.format(username)) as f:
        posts = json.loads(f.read())
        post = filter(lambda x: x['id'] == post_id, posts)
        if post:
            return post[0]
        else:
            raise Exception("Post not found!")

def writeFile(data, file_out):
    with open(file_out_dir + file_out, 'w') as f:
        f.write(data)
        f.flush()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        flash('Label saved', 'info')
        writeFile(json.dumps(dict(zip(request.form.getlist('id[]'), request.form.getlist('label[]')))), request.form.get('filename'))
        return redirect('/')
    data, f = getComments()
    username, post_id = f.split(' ')
    post_id = post_id[:-5]
    post = getPost(username, post_id)
    return render_template('index.html', data=data, post=post, filename=f)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
