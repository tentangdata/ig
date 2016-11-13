import cPickle as pickle
import json
import pandas as pd
import os

LABEL_DIR = '/home/aliakbars/Dropbox/Spam/label/'
COMMENTS_DIR = '/home/aliakbars/Dropbox/Spam/comments/'
POSTS_DIR = '/home/aliakbars/Dropbox/Spam/posts_160923/'

df = pd.DataFrame()
for f in os.listdir(LABEL_DIR):
    labels = json.loads(open(LABEL_DIR + f).read())
    labels = pd.DataFrame(zip(labels.keys(), labels.values()), columns=['id', 'label'])

    comments = json.loads(open(COMMENTS_DIR + f).read())
    comments = pd.DataFrame(comments)
    merged = pd.merge(comments, labels, on='id')

    filename, post_id = f.split(' ')
    post_id = post_id.split('.')[0]
    posts = pd.read_json(POSTS_DIR + filename + '.json')
    merged['post_id'] = post_id

    merged = pd.merge(merged, posts, left_on='post_id', right_on='id', suffixes=['', '_post'])
    df = pd.concat([df, merged])
df.to_pickle('/home/aliakbars/Dropbox/Spam/data-post.p')