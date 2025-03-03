from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from datetime import datetime
from flask import Flask, render_template, jsonify
from urllib.parse import quote_plus

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
    return render_template("index.html")

# API to Fetch Latest Posts
@app.route("/get_posts")
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    return jsonify([{"title": post.title, "content": post.content} for post in posts])


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)
    
# ipconfig -> 127.0.0.1:8080 , 192.168.1.10:8080
