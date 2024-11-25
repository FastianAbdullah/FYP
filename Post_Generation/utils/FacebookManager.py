import requests
import streamlit as st
from typing import List,Dict,Optional

#Class To Handle FaceBook Operations.
class FacebookManager:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_pages(self) -> List[Dict]:
        """Get list of Facebook pages managed by the user"""
        pages_url = "https://graph.facebook.com/v20.0/me/accounts"
        params = {
            "access_token": self.access_token,
            "fields": "name,id,access_token"
        }
        try:
            response = requests.get(pages_url, params=params)
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            st.error(f"Error getting user pages: {str(e)}")
            return []

    def post_content(self, page_id: str, page_token: str, image_url: str, message: str) -> Optional[Dict]:
        """Post image with message to Facebook page"""
        post_url = f'https://graph.facebook.com/v20.0/{page_id}/photos'
        data = {
            'url': image_url,
            'message': message,
            'access_token': page_token
        }
        try:
            response = requests.post(post_url, data=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error posting to Facebook: {str(e)}")
            return None

