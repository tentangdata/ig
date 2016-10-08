from accessors import CommentFileAccessor, PostFileAccessor
from app import app_config
import json


class MainService(object):
    def __init__(self):
        self.app_config = app_config
        self._comment_accessor = CommentFileAccessor(
            self.app_config.file_in_dir,
            self.app_config.file_out_dir
        )
        self._post_accessor = PostFileAccessor(
            self.app_config.posts_dir
        )

    def get_comments(self):
        return self._comment_accessor.get_comments()

    def get_post(self, username, post_id):
        return self._post_accessor.get_post(
            username,
            post_id
        )

    def write_comment(self, id_list, label_list, filename):

        self._comment_accessor.write_comment(
            json.dumps(
                dict(
                    zip(
                        id_list,
                        label_list
                    )
                )
            ),
            filename
        )
