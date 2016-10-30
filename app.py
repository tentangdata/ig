from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from helpers import AppConfigParser


app = Flask(__name__)
app.secret_key = 'instagram-screen-scraper'
app_config = AppConfigParser().parse()
app.config['SQLALCHEMY_DATABASE_URI'] = app_config.get_db_url()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)





