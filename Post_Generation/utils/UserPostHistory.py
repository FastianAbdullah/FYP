from typing import Dict,List
from datetime import datetime
import streamlit as st

class UserPostHistory:
    def __init__(self):
        if 'post_history' not in st.session_state:
            st.session_state.post_history = []

    def add_post(self, platform: str, post_data: Dict):
        """Add a new post to history"""
        post_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'platform': platform,
            'data': post_data
        }
        st.session_state.post_history.append(post_entry)

    def get_history(self) -> List[Dict]:
        """Get all posts from history"""
        return st.session_state.post_history