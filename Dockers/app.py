from flask import Flask , render_template,url_for 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) 

@app.route('/',methods=['GET'])
def home():
    return 'http://localhost'
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)