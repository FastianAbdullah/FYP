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
REDIRECT_URI = 'https://localhost:5000/callback'

@app.route('/')
def index():
    return render_template_string('''
        <h1>Social Media Image Poster</h1>
        {% if session.get('access_token') %}
            <p>You are logged in. Access token: {{ session.get('access_token')[:10] }}...</p>
            <p>Page ID: {{ session.get('page_id') }}</p>
            <p>Instagram User ID: {{ session.get('ig_user_id') }}</p>
            <p><a href="/post_image">Post an image</a></p>
        {% else %}
            <p>Not logged in.</p>
            <a href="/login">Login with Facebook</a>
        {% endif %}
    ''')


@app.route('/login')
def login():
    permissions = "pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish"
    return redirect(f"https://www.facebook.com/v20.0/dialog/oauth?client_id={APP_ID}&redirect_uri={REDIRECT_URI}&scope={permissions}")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={APP_ID}&redirect_uri={REDIRECT_URI}&client_secret={APP_SECRET}&code={code}"
    
    response = requests.get(token_url)
    access_token = response.json().get('access_token')
    
    if access_token:
        # Store the access_token in the session
        session['access_token'] = access_token

        # Get user's pages
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={access_token}"
        pages_response = requests.get(pages_url)
        pages = pages_response.json().get('data', [])
        
        if pages:
            # Store the first page's access token
            session['page_token'] = pages[0]['access_token']
            session['page_id'] = pages[0]['id']
            
            # Get Instagram Business Account ID
            ig_account_url = f"https://graph.facebook.com/v20.0/{pages[0]['id']}?fields=instagram_business_account&access_token={pages[0]['access_token']}"
            ig_response = requests.get(ig_account_url)
            ig_data = ig_response.json()
            
            if 'instagram_business_account' in ig_data:
                session['ig_user_id'] = ig_data['instagram_business_account']['id']
            else:
                return 'No Instagram Business Account found. Make sure you have connected an Instagram account to your Facebook Page.'
        else:
            return 'No pages found. Make sure you have a Facebook Page.'
        
        return redirect('/')
    else:
        return 'Login failed.'

@app.route('/post_image')
def post_image():
    page_token = session.get('page_token')
    page_id = session.get('page_id')
    ig_user_id = session.get('ig_user_id')
    if not page_token or not page_id or not ig_user_id:
        return redirect('/login')

    image_path = 'Testing_apis\posting\windows.PNG'  # Ensure this file exists in your project directory
    message = "Automated Posting with an Image"

    img_url = "https://www.shutterstock.com/image-photo/sitting-sweety-cat-looking-aside-600nw-2323092103.jpg"
    caption = "#BronzFonz"

    # Post to Facebook
    fb_result = post_to_facebook(page_id, page_token, image_path, message)

    # Post to Instagram
    ig_result = post_to_instagram(ig_user_id, page_token, img_url, caption)

    return f"Facebook: {fb_result}<br>Instagram: {ig_result}"

def post_to_facebook(page_id, page_token, image_path, message):
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

def post_to_instagram(ig_user_id, access_token, image_path, caption):
    # Step 1: Create the media container
    media_url = f'https://graph.facebook.com/v20.0/{ig_user_id}/media'
    
    # Upload image to a publicly accessible URL (you may need to implement this)
    image_url = upload_image_to_public_url(image_path)
    
    media_params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }

    response = requests.post(media_url, params=media_params)
    result = response.json()

    if 'id' in result:
        creation_id = result['id']
        
        # Step 2: Publish the media container
        publish_url = f'https://graph.facebook.com/v20.0/{ig_user_id}/media_publish'
        publish_params = {
            'creation_id': creation_id,
            'access_token': access_token
        }

        publish_response = requests.post(publish_url, params=publish_params)
        publish_result = publish_response.json()

        if 'id' in publish_result:
            return f"Instagram media published successfully with ID: {publish_result['id']}"
        else:
            return f"Error publishing media on Instagram: {publish_result}"
    else:
        return f"Error creating media container for Instagram: {result}"

def upload_image_to_public_url(image_path):
    return "https://www.shutterstock.com/image-photo/sitting-sweety-cat-looking-aside-600nw-2323092103.jpg"

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')