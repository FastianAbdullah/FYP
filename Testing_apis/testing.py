from flask import Flask, redirect, request, session, render_template_string
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890987654"
if not app.secret_key:
    raise ValueError("No secret key set for Flask application")

# Facebook App credentials
APP_ID = '946777884128732'
APP_SECRET = 'bcf73367d2254b06455c523fbfadd14c'
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def index():
    return render_template_string('''
        <h1>Facebook Image Poster</h1>
        {% if session.get('access_token') %}
            <p>You are logged in. <a href="/post_image">Post an image</a></p>
        {% else %}
            <a href="/login">Login with Facebook</a>
        {% endif %}
    ''')

@app.route('/login')
def login():
    permissions = "pages_read_engagement,pages_manage_posts"
    return redirect(f"https://www.facebook.com/v20.0/dialog/oauth?client_id={APP_ID}&redirect_uri={REDIRECT_URI}&scope={permissions}")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={APP_ID}&redirect_uri={REDIRECT_URI}&client_secret={APP_SECRET}&code={code}"
    
    response = requests.get(token_url)
    access_token = response.json().get('access_token')
    
    if access_token:
        # Get user's pages
        print("access_token",access_token)
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={access_token}"
        pages_response = requests.get(pages_url)
        pages = pages_response.json().get('data', [])
        
        if pages:
            # Store the first page's access token
            session['page_token'] = pages[0]['access_token']
            session['page_id'] = pages[0]['id']
        else:
            return 'No pages found. Make sure you have a Facebook Page.'
        
        return redirect('/')
    else:
        return 'Login failed.'

@app.route('/post_image')
def post_image():
    page_token = session.get('page_token')
    page_id = session.get('page_id')
    if not page_token or not page_id:
        return redirect('/login')

    image_path = 'ok.PNG'  # Ensure this file exists in your project directory
    message = "Automated Posting with an Image"

    post_url = f'https://graph.facebook.com/v20.0/{page_id}/photos'

    data = {
        'message': message,
        'access_token': page_token
    }

    with open(image_path, 'rb') as image_file:
        files = {
            'source': image_file
        }

        response = requests.post(post_url, data=data, files=files)

    if response.status_code == 200:
        return "Image posted successfully!"
    else:
        return f"Error posting image: {response.text}"

if __name__ == '__main__':
    app.run(debug=True)