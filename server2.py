from flask import Flask,render_template
import datetime
from flask_sqlalchemy import SQLAlchemy as sq

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///resume.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = sq(app)

@app.route("/")
def main_page():
    return render_template("./templates/index.html",date=datetime.date.today().year)

class Images(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    file_name = db.Column(db.String, nullable = False)

with app.app_context():
    db.create_all()

def table_setup():
    file_path = "./static/images/title.txt"
    title = []
    with open(file_path, 'r') as file:
        for line in file:
            title.append(line.strip())
    id =0
    with app.app_context():
        for i in range(len(title)):
            filename = "HM_"+str(i)+".jpg"
            new_image = Images(title=title[i],file_name=filename)
            db.session.add(new_image)
            db.session.commit()
            id = id+1
        
#table_setup()

@app.route("/myGallery")
def photo_page():
    all_images= db.session.query(Images).all()
    return render_template("./templates/photo_gallery.html",date=datetime.date.today().year,images=all_images)

@app.route("/nav")
def nav():
    return render_template("./templates/nav_bar.html",date=datetime.date.today().year)

@app.route("/blog")
def blog():
    return render_template("./templates/blog.html",date=datetime.date.today().year)

if __name__ == "__main__":
    app.run(debug=True)
