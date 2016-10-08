import json
import os
import random
from models import Comments


class CommentAccessor(object):
    def __init__(self):
        pass

    def get_unannotated_comment(self):
        pass

    def insert_comment(self):
        pass

    def update_label(self):
        pass

    def get_comments(self):
        pass


class CommentFileAccessor(CommentAccessor):

    def __init__(self, file_in_dir, file_out_dir):
        super(CommentFileAccessor, self).__init__()
        self.file_in_dir = file_in_dir
        self.file_out_dir = file_out_dir

    def get_comments(self):
        file_in = os.listdir(self.file_in_dir)
        file_out = os.listdir(self.file_out_dir)
        f = random.sample(set(file_in) - set(file_out), 1)[0]
        return json.loads(open(self.file_in_dir + f).read())[:50], f

    def write_comment(self, file_out, data):
        f = open(self.file_out_dir + file_out, 'w')
        f.write(data)
        f.flush()


class PostAccessor(object):
    def __init__(self):
        pass

    def get_post(self, username, post_id):
        pass


class PostFileAccessor(PostAccessor):
    def __init__(self, post_dir):
        super(PostFileAccessor, self).__init__()
        self.post_dir = post_dir

    def get_post(self, username, post_id):
        f = open(self.post_dir + '{}.json'.format(username))
        posts = json.loads(f.read())
        post = filter(lambda x: x['id'] == post_id, posts)
        if post:
            return post[0]
        else:
            raise Exception("Post not found!")

