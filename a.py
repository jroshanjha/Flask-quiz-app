# 🔹 1. Cookies in Flask
# Cookies are small pieces of data stored in the user's browser.

# 🔹 2. Session in Flask
# Flask's session uses signed cookies to store user session data. This data is stored client-side, but Flask signs it to ensure it can't be modified without detection.


from flask import Flask, request, make_response
from flask import Flask, session, redirect, url_for, request


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to sign session cookies

@app.route('/')
def index():
    return request.cookies.get('username')
@app.route('/set_cookie')
def set_cookie():
    resp = make_response("Cookie is set")
    session['username'] = 'jroshan'
    resp.set_cookie('username', session.get('username'))
    
    return resp

@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Logged in as {username}'



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('profile'))
    return '''
        <form method="post">
            <input type="text" name="username">
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/profile')
def profile():
    username = session.get('username')
    if username:
        return f'Welcome back, {username}!'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)