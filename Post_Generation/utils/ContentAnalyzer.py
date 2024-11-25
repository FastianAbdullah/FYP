import requests
from collections import Counter
import re
import streamlit as st
from typing import List,Dict

#Class to filter Top Posts From SocialMedia Handles.
class ContentAnalyzer:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_top_posts(self, ig_user_id: str, hashtag: str, limit: int = 50) -> List[Dict]:
        """Fetch top posts for a given hashtag"""
        hashtag_search_url = "https://graph.facebook.com/v20.0/ig_hashtag_search"
        params = {
            "user_id": ig_user_id,
            "q": hashtag.strip('#'),
            "access_token": self.access_token
        }
        
        try:
            response = requests.get(hashtag_search_url, params=params)
            response.raise_for_status()
            hashtag_data = response.json()
            
            if 'data' in hashtag_data and hashtag_data['data']:
                hashtag_id = hashtag_data['data'][0]['id']
                
                # Get top media for the hashtag
                top_media_url = f"https://graph.facebook.com/v20.0/{hashtag_id}/top_media"
                media_params = {
                    "user_id": ig_user_id,
                    "fields": "caption,like_count,comments_count,media_type,permalink,media_url",
                    "access_token": self.access_token,
                    "limit": limit
                }
                
                media_response = requests.get(top_media_url, params=media_params)
                media_response.raise_for_status()
                return media_response.json().get('data', [])
            
            return []
        except Exception as e:
            st.error(f"Error fetching top posts: {str(e)}")
            return []

    def get_top_performing_posts(self, posts: List[Dict], num_posts: int = 2) -> List[Dict]:
        """Get top performing posts based on engagement"""
        if not posts:
            return []
            
        # Calculate engagement score for each post
        for post in posts:
            post['engagement_score'] = (
                post.get('like_count', 0) + 
                (post.get('comments_count', 0) * 2)  # Comments weighted more heavily
            )
        
        # Sort posts by engagement score
        sorted_posts = sorted(
            posts, 
            key=lambda x: x.get('engagement_score', 0), 
            reverse=True
        )
        
        # Return top posts with their captions cleaned
        top_posts = []
        for post in sorted_posts[:num_posts]:
            if post.get('caption'):
                top_posts.append({
                    'caption': post['caption'],
                    'likes': post.get('like_count', 0),
                    'comments': post.get('comments_count', 0),
                    'engagement_score': post['engagement_score'],
                    'permalink': post.get('permalink', '')
                })
        
        return top_posts

    def analyze_descriptions(self, posts: List[Dict]) -> Dict:
        """Analyze post descriptions to extract patterns and insights"""
        analysis = {
            'avg_length': 0,
            'common_phrases': [],
            'emoji_usage': {},
            'common_words': [],
            'engagement_correlation': {},
            'structure_patterns': {
                'has_emoji': 0,
                'has_hashtags': 0,
                'has_mentions': 0,
                'has_call_to_action': 0
            },
            'top_performing_posts': self.get_top_performing_posts(posts)
        }
        
        if not posts:
            return analysis
            
        total_length = 0
        all_words = []
        phrases = []
        emojis = []
        
        # Common call to action phrases
        cta_patterns = [
            'check out', 'click', 'tap', 'swipe up', 'link in bio',
            'follow', 'share', 'like', 'comment', 'tag', 'tell us'
        ]
        
        for post in posts:
            caption = post.get('caption', '')
            if not caption:
                continue
                
            # Length analysis
            total_length += len(caption)
            
            # Emoji analysis
            post_emojis = re.findall(r'[\U0001F300-\U0001F9FF]', caption)
            emojis.extend(post_emojis)
            
            # Word analysis
            words = re.findall(r'\b\w+\b', caption.lower())
            all_words.extend(words)
            
            # Extract 2-3 word phrases
            words = caption.lower().split()
            for i in range(len(words)-1):
                phrases.append(f"{words[i]} {words[i+1]}")
                if i < len(words)-2:
                    phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
            
            # Structure analysis
            if post_emojis:
                analysis['structure_patterns']['has_emoji'] += 1
            if '#' in caption:
                analysis['structure_patterns']['has_hashtags'] += 1
            if '@' in caption:
                analysis['structure_patterns']['has_mentions'] += 1
            if any(cta in caption.lower() for cta in cta_patterns):
                analysis['structure_patterns']['has_call_to_action'] += 1
        
        # Calculate averages and percentages
        num_posts = len(posts)
        analysis['avg_length'] = total_length / num_posts if num_posts > 0 else 0
        
        # Get most common words (excluding common stop words)
        stop_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 
                     'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at'}
        word_counts = Counter(word for word in all_words if word not in stop_words)
        analysis['common_words'] = word_counts.most_common(10)
        
        # Get most common phrases
        phrase_counts = Counter(phrases)
        analysis['common_phrases'] = phrase_counts.most_common(5)
        
        # Get emoji usage
        emoji_counts = Counter(emojis)
        analysis['emoji_usage'] = dict(emoji_counts.most_common(5))
        
        # Convert structure patterns to percentages
        for key in analysis['structure_patterns']:
            analysis['structure_patterns'][key] = (
                analysis['structure_patterns'][key] / num_posts * 100
            )
        
        return analysis

    def generate_description_template(self, analysis: Dict) -> str:
        """Generate a description template based on analysis"""
        template = ""
        
        # Add popular phrases
        if analysis['common_phrases']:
            phrase = analysis['common_phrases'][0][0]
            template += f"{phrase.title()} "
        
        # Add popular emojis
        if analysis['emoji_usage']:
            emojis = list(analysis['emoji_usage'].keys())[:2]
            template += f"{' '.join(emojis)} "
        
        # Add call to action if commonly used
        if analysis['structure_patterns']['has_call_to_action'] > 50:
            template += "\n\nDouble tap if you love this! 💕 "
        
        # Add mention suggestion if commonly used
        if analysis['structure_patterns']['has_mentions'] > 50:
            template += "\nTag someone who needs to see this! "
        
        # Add hashtag placeholder
        if analysis['structure_patterns']['has_hashtags'] > 50:
            template += "\n\n#[relevanthashtag] #[niche] #[branded] "
        
        return template.strip()
