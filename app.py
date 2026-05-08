from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
import credentials

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

oauth = OAuth(app)


github = oauth.register(
name='github',
client_id=credentials.client_id,
client_secret=credentials.client_secret,

access_token_url='https://github.com/login/oauth/access_token',

authorize_url='https://github.com/login/oauth/authorize',
api_base_url='https://api.github.com/',
client_kwargs={'scope': 'user:email'},
)

@app.route("/login")
def login():
    redirect_uri = url_for('callback', _external=True) 
    return github.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    user = github.get('user')
    session['user'] = user.json()
    return redirect("/profile")

@app.route("/profile")
def profile():
    if 'user' not in session:
        return "Unauthorized"
    return f"Welcome,  {session.get('user').get('login')}! <br> <img src='{session.get('user').get('avatar_url')}'> <br> <a href='/logout'>Logout</a>"
    
@app.route("/logout")
def logout():
    
    session.pop('user', None)
    return redirect('/profile')


if __name__ == '__main__':
    app.run(debug=True)
