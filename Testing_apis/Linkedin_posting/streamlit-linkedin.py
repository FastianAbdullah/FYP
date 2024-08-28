import streamlit as st
import requests
from urllib.parse import urlencode
import webbrowser
# from dotenv import load_dotenv

# load_dotenv()
# LinkedIn API configuration
CLIENT_ID = st.secrets["LK_CLIENT_ID"]
CLIENT_SECRET = st.secrets["LK_CLIENT_SECRET"]
REDIRECT_URI = "https://linkedin-autoposting.streamlit.app/"  # Streamlit default local URL

# LinkedIn API endpoints
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
PROFILE_URL = "https://api.linkedin.com/v2/userinfo"
COMPANY_URL = "https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee"
POST_URL = "https://api.linkedin.com/v2/ugcPosts"

def get_authorization_url():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile w_member_social email"
    }
    return f"{AUTH_URL}?{urlencode(params)}"

def get_access_token(code):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json().get("access_token")

def get_user_profile(access_token):
    # print(access_token)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(PROFILE_URL, headers=headers)
    print(f'Profile Details:{response.json()}')
    return response.json()

def get_user_companies(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(COMPANY_URL, headers=headers)
    print(f'USER COMPANIES: {response.json()}')
    companies = response.json().get("elements", [])
    return [{"id": company["organizationalTarget"].split(":")[-1], "name": company["organizationalTarget"]} for company in companies]

def post_to_linkedin(access_token, content, is_company_post=False, company_id=None):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    author = f"urn:li:organization:{company_id}" if is_company_post else f"urn:li:person:{get_user_profile(access_token)['sub']}"
    
    post_data = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    
    response = requests.post(POST_URL, json=post_data, headers=headers)
    return response.json()

def main():
    st.title("LinkedIn Integration")

    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    if st.session_state.access_token is None:
        if "code" not in st.query_params:
            auth_url = get_authorization_url()
            st.write("Click the button below to connect with LinkedIn")
            if st.button("Connect with LinkedIn"):
                webbrowser.open_new_tab(url=auth_url)
                # st.markdown(auth_url)
        else:
            code = st.query_params["code"]
            st.session_state.access_token = get_access_token(code)
            st.rerun()
    else:
        st.success("Connected to LinkedIn")
        
        user_profile = get_user_profile(st.session_state.access_token)
        st.write(f"Welcome, {user_profile['given_name']} {user_profile['family_name']}!")

        companies = get_user_companies(st.session_state.access_token)
        post_options = ["Personal Profile"] + [company["name"] for company in companies]
        
        post_target = st.selectbox("Select where to post", post_options)
        post_content = st.text_area("Enter your post content")
        
        if st.button("Post to LinkedIn"):
            if post_content:
                try:
                    if post_target == "Personal Profile":
                        result = post_to_linkedin(st.session_state.access_token, post_content)
                    else:
                        company_id = next(company["id"] for company in companies if company["name"] == post_target)
                        result = post_to_linkedin(st.session_state.access_token, post_content, True, company_id)
                    st.success("Posted successfully to LinkedIn!")
                except Exception as e:
                    st.error(f"Error posting to LinkedIn: {str(e)}")
            else:
                st.warning("Please enter some content for your post.")

if __name__ == "__main__":
    main()