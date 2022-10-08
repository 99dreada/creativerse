from flask import Flask
from flask_assets import Environment, Bundle
from flask.cli import AppGroup
import os

from PANEL.model import db

app = Flask(__name__)

def config_db(db_url='sqlite:///db/panel.db'):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if app.config.get('PROFILE', False): # pragma: no cover
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.secret_key = "#########"
    db.init_app(app)

def config_sass():
    #Converting Sass file to Css
    scss = Bundle('scss/main.scss', filters='pyscss', output='styles/css/main.css')
    #SCSS Connection
    assets = Environment(app)
    # assets.url= app.static_url_path
    assets.debug=True
    assets.register('scss_main', scss)

config_sass()
config_db()

from PANEL import routes

db_cli = AppGroup('db')

@db_cli.command('init')
def db_init():
    try: os.mkdir('PANEL/db')
    except: pass
    from PANEL.model import create_db
    create_db()

app.cli.add_command(db_cli)