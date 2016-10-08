#!/usr/bin/python
from flask import flash, render_template, request, redirect
from app import app, manager
from services import MainService


main_service = MainService()


class IgApp(object):
    @staticmethod
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            flash('Label saved', 'info')
            main_service.write_comment(
                request.form.getlist('id[]'),
                request.form.getlist('label[]'),
                request.form.get('filename')
            )
            return redirect('/')
        data, f = main_service.get_comments()
        username, post_id = f.split(' ')
        post_id = post_id[:-5]
        post = main_service.get_post(username, post_id)
        return render_template('index.html', data=data, post=post, filename=f)


if __name__ == '__main__':
    manager.run()