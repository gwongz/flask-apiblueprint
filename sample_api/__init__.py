from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    firstname = db.Column(db.String(60))

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(60))

@app.route('/')
def index():
    return render_template('index.html')

def seed_db():
    user = User(username='gimmecat', firstname='Cat')
    user2 = User(username='gimmefish', firstname='Fish')
    media = Media(kind='photo')
    db.session.add_all([user, user2, media])
    db.session.commit()

def create_app():
    db.drop_all()
    db.create_all()
    seed_db()
    from sample_api.views.v1 import api_v1
    app.register_blueprint(api_v1)
    from sample_api.views.v2 import api_v2
    app.register_blueprint(api_v2)






