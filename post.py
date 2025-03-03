from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from datetime import datetime
from flask import Flask, render_template, jsonify,request,render_template
from urllib.parse import quote_plus
import logging_config  # Automatically sets up logging

app = Flask(__name__)
# MySQL Configuration
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'jroshan@98'
# app.config['MYSQL_DB'] = 'quiz_app'

# URL encode the password
password = quote_plus('jroshan@98')


# MySQL Configuration with properly encoded password
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{password}@localhost/quiz_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    _user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    phone = db.Column(db.String(255),nullable=False)
    username = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    address = db.Column(db.String(255),nullable=False)
    comment = db.Column(db.String(255),nullable=True) # Text
    created_at = db.Column(db.DateTime(),nullable=True)
    update_at = db.Column(db.DateTime(),nullable=True)
    
# Initialize Database
with app.app_context():
    db.create_all()
    
# with app.app_context():
#     db.session.add(Post(title="First Post", content="This is the first post."))
#     db.session.add(Post(title="Second Post", content="This is the second post."))
#     db.session.commit()

# Route to Serve HTML Page
@app.route("/admin/", methods=['GET'])
def admin():
    return 'This is admin page.'
    #return render_template("admin.html")
@app.route('/admin/dash', methods=['GET'])
def dash():
    return render_template('dash.html')
# Route to Serve HTML Page
@app.route("/")
def home():
    new_user = User(
    name="John Doe",
    email="john@example.com",
    phone="1234567890",
    username="johndoe",
    password="hashed_password",  # Always hash passwords in real applications
    address="123 Main St",
    comment="First user",
    created_at=datetime.utcnow(),
    update_at=datetime.utcnow())
    db.session.add(new_user)
    db.session.commit()
    
    # 1. Create a new user
    new_user = User(
        name="John Doe",
        email="john@example.com",
        phone="1234567890",
        username="johndoe",
        password="hashedpassword",  # Remember to hash passwords!
        address="123 Main St",
        created_at=datetime.utcnow()
    )
    db.session.add(new_user)
    db.session.commit()
    return render_template("index.html")

# API to Fetch Latest Posts
@app.route('/add_posts',methods=['POST'])
def add_posts():
    # data = request.json['data']
    data = request.json
    #return jsonify(data)
    post = Post(title=data['title'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post added successfully'})


# API to Fetch Latest Posts
@app.route('/add_user', methods=['POST'])
def add_user_posts():
    data = request.json
    if data['comment']:
        user = User(name=data['name'], email=data['email'], phone=data['phone'], username=data['username'], password=data['password'], address=data['address'], comment=data['comment'],created_at =datetime.now(),updated_at=datetime.now())
    else:
        #data = request.get_json(force=True)
        user = User(name=data['name'], email=data['email'], phone=data['phone'], username=data['username'], password=data['password'], address=data['address'],created_at =datetime.now(),updated_at=datetime.now())
    db.session.add(user)
    db.session.commit()
    
@app.route('/admin/get_users',methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email, 'phone': user.phone, 'username': user.username,'password': user.password,'address': user.address,'comment': user.comment} for user in users])

@app.route("/get_posts")
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    return jsonify([{"title": post.title, "content": post.content} for post in posts])

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)
    
# ipconfig -> 127.0.0.1:8080 , 192.168.1.10:8080
    