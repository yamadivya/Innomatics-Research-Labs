import os
from flask import Flask, app, render_template, request, redirect, url_for
from flask.helpers import flash
from flask.templating import render_template
from hashids import Hashids
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this should be a secret random string'
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir, 'schema.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)

class URL(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text)
    short_url = db.Column(db.Text)
    def __init__(self, original_url, short_url):
        self.original_url=original_url
        self.short_url=short_url

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

@app.route('/')
def home_get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def home_post():
    o_url=request.form.get('in_1')
    hashid = hashids.encode(len(o_url))
    s_url = request.host_url + hashid
    print(s_url)
    new_url=URL(o_url,s_url)
    url_data = db.session.add(new_url)
    db.session.commit()    
    return render_template('index.html', short_url=s_url)

@app.route('/history')
def history_get():
    db_urls=URL.query.all()
    return render_template('history.html', urls=db_urls)

@app.route('/<id>')
def url_redirect(id):
    for i in db.session.execute("SELECT original_url FROM urls WHERE short_url='{}'".format("http://127.0.0.1:5000/"+id)):
        return redirect(i[0])
        
if __name__ == '__main__':
    app.run(debug=True)