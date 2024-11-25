import streamlit as st
import requests
from typing import Optional

#Class to Get Permission for Posting on Behalf of User.
class SocialMediaAuth:
    def __init__(self, app_id: str, app_secret: str, redirect_uri: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri

    def generate_auth_url(self, platform: str) -> str:
        """Generate authentication URL for Facebook or Instagram"""
        permissions = {
            'facebook': "pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish",
            'instagram': "instagram_basic,instagram_content_publish"
        }
        return f"https://www.facebook.com/v20.0/dialog/oauth?client_id={self.app_id}&redirect_uri={self.redirect_uri}&scope={permissions[platform]}"

    def get_access_token(self, code: str) -> Optional[str]:
        """Exchange authorization code for access token"""
        token_url = "https://graph.facebook.com/v20.0/oauth/access_token"
        params = {
            "client_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "client_secret": self.app_secret,
            "code": code
        }
        try:
            response = requests.get(token_url, params=params)
            response.raise_for_status()
            return response.json().get('access_token')
        except Exception as e:
            st.error(f"Error getting access token: {str(e)}")
            return None
