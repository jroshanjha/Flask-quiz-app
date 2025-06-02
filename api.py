from flask import Flask,request,jsonify,redirect,url_for,flash,session,render_template,abort
from flask_restful import Resource, Api, reqparse
import logging
import logging_config
import mysql.connector

users = [
    {"id": 1, "name": "John", "age": 30,"email": "john@example.com"},
    {"id": 2, "name": "Alice", "age": 25,"email": "alice@example.com"},
    {"id": 3, "name": "Bob", "age": 40,"email": "bob@example.com"},
]

# Applications
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


# Routes
@app.route('/',methods=['GET'])
def index():
    return "Hello, World!"

# testing 
@app.route('/joyti',methods=['GET'])
def joyti():
    return "Hello, World!- JOYTI"
@app.route('/joyti-name',methods=['GET'])
def joyti_name():
    return "Hello, World!- JOYTI Name!"
@app.route('/users',methods=['GET'])
def index_users():
    return jsonify(users),201

@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    info =''
    for user in users:
        if user['id']==user_id:
            info = user 
    if info is None:
        return jsonify({'error':'User not found'}),404
    else:
         return jsonify(info),201
    # user = next((user for user in users if user['id'] == user_id), None)
    # return jsonify(user) if user else ('', 404)
    
@app.route('/users',methods=['POST'])
def add_user():
    #data = request.get_json(force=True)
    data = request.json['data']
    data['id']= users[-1]['id'] + 1
    if not data or not 'id' in data or not 'name' in data or not 'age' in data:
        abort(404)
    users.append(data)
    return jsonify(data),201
## api.py , api.mysql , api.doc, api.xmls or api.csv
#3 a
@app.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    data = request.get_json(force=True)
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        user['name'] = data['name']
        user['age'] = data['age']
        user['email'] = data['email']
        user.update(data)
        return jsonify(user),201
    else:
        return jsonify({'error':'User not found'}),404
    
@app.route('/users/<int:id>',methods=['DELETE'])
def delete(id):
    for user in users:
        if user['id'] == id:
            users.remove(user)
            return jsonify(user),201
        else:
            return jsonify({'error':'User not found'}),404
    
if __name__=='__main__':
    app.run(debug=True)




# {"data":{
#   "name":"jroshan",
#   "age":28,
#   "email":"jroshancode@gmail.com"
# }
# }

# {
#   "name":"jroshan",
#   "age":28,
#   "email":"jroshancode@gmail.com"
# }

