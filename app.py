from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///img.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    minetype = db.Column(db.Text, nullable=False)


@app.route('/')
def hello():
    return "Hello Sam"

@app.route('/upload', methods=[ 'GET' ,'POST'] )
def upload():

    if request.method=="POST":
        pic = request.files['pic']
    
        if not pic:
            return "No Pic uploaded"
        
        filename = secure_filename(pic.filename)
        minetype = pic.mimetype

        img = Img(img = pic.read(), minetype=minetype, name=filename )
        db.session.add(img)
        db.session.commit()

    allimg = Img.query.all()

    return render_template("index.html", allimg=allimg)

if __name__=="__main__":
    app.run(debug=True)