from typing import List,Dict,Optional,Tuple
from collections import Counter
import requests
import re
import streamlit as st

#Class To handle Instagram Operations.
class InstagramManager:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_accounts(self) -> List[Dict]:
        """Get list of Instagram business accounts"""
        ig_accounts_url = "https://graph.facebook.com/v20.0/me/accounts"
        params = {
            "fields": "instagram_business_account{id,name,username}",
            "access_token": self.access_token
        }
        try:
            response = requests.get(ig_accounts_url, params=params)
            response.raise_for_status()
            data = response.json().get('data', [])
            accounts = []
            for account in data:
                if 'instagram_business_account' in account:
                    ig_account = account['instagram_business_account']
                    accounts.append({
                        'id': ig_account['id'],
                        'name': ig_account.get('name', 'Unknown'),
                        'username': ig_account.get('username', 'Unknown')
                    })
            return accounts
        except Exception as e:
            st.error(f"Error getting Instagram accounts: {str(e)}")
            return []

    def post_content(self, ig_user_id: str, image_url: str, caption: str) -> Optional[Dict]:
        """Post image with caption to Instagram business account"""
        media_url = f'https://graph.facebook.com/v20.0/{ig_user_id}/media'
        media_params = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.access_token
        }
        try:
            response = requests.post(media_url, params=media_params)
            response.raise_for_status()
            result = response.json()
            
            if 'id' in result:
                creation_id = result['id']
                publish_url = f'https://graph.facebook.com/v20.0/{ig_user_id}/media_publish'
                publish_params = {
                    'creation_id': creation_id,
                    'access_token': self.access_token
                }
                publish_response = requests.post(publish_url, params=publish_params)
                publish_response.raise_for_status()
                return publish_response.json()
            return result
        except Exception as e:
            st.error(f"Error posting to Instagram: {str(e)}")
            return None

    def get_trending_hashtags(self, ig_user_id: str, seed_hashtag: str) -> List[Tuple[str, int]]:
        """Get trending hashtags based on a seed hashtag"""
        hashtag_search_url = "https://graph.facebook.com/v20.0/ig_hashtag_search"
        params = {
            "user_id": ig_user_id,
            "q": seed_hashtag.strip('#'),
            "access_token": self.access_token
        }
        
        try:
            response = requests.get(hashtag_search_url, params=params)
            response.raise_for_status()
            hashtag_data = response.json()
            
            if 'data' in hashtag_data and hashtag_data['data']:
                hashtag_id = hashtag_data['data'][0]['id']
                
                media_url = f"https://graph.facebook.com/v20.0/{hashtag_id}/recent_media"
                media_params = {
                    "user_id": ig_user_id,
                    "fields": "caption,like_count,comments_count",
                    "access_token": self.access_token,
                    "limit": 50
                }
                
                media_response = requests.get(media_url, params=media_params)
                media_response.raise_for_status()
                media_data = media_response.json()
                
                all_hashtags = []
                if 'data' in media_data:
                    for post in media_data['data']:
                        if 'caption' in post:
                            hashtags = re.findall(r'#\w+', post['caption'])
                            weight = 1 + (post.get('like_count', 0) + post.get('comments_count', 0)) / 100
                            all_hashtags.extend([hashtag for hashtag in hashtags] * int(weight))
                
                hashtag_counts = Counter(all_hashtags)
                if f"#{seed_hashtag.strip('#')}" in hashtag_counts:
                    del hashtag_counts[f"#{seed_hashtag.strip('#')}"]
                
                return hashtag_counts.most_common(15)
                
        except Exception as e:
            st.error(f"Error fetching trending hashtags: {str(e)}")
            return []
