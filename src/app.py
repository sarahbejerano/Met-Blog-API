from flask import Flask, jsonify,request
from sqlalchemy import create_engine
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, String, Float
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/example' 
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

SQLAlchemy(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.Integer, unique=True, nullable=False)
    favorites = db.Column(db.String (20))


    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, email, password,favorites):
        self.username = username
        self.email = email
        self.password = password
        self.favorites = favorites

db.create_all()

class User_Schema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "password", "favorites")


user_schema = User_Schema()
users_schema = User_Schema(many=True)

@app.route('/create_user', methods=['POST'])
def create_user():
    print(request.json)
    return 'received'


@app.route('/objects', methods=["GET"])
def get_objects():
    return requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects').json()


@app.route('/objects/<int:id>', methods=["GET"])
def get_objects_by_id(id):
    result = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/'+ str(id)).json()

    return {
    "objectID":result["objectID"],
    "title":result["title"],
    "primaryImage":result["primaryImage"],
    "objectDate": result["objectDate"]
    }






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)