import streamlit as st
import requests
from collections import Counter
import re
import json
from datetime import datetime
import time
from typing import List, Dict, Tuple, Optional

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

class PostHistory:
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

class SocialMediaApp:
    def __init__(self):
        self.config = {
            "page_title": "Social Media Image Poster",
            "page_icon": "📷",
            "layout": "wide",
            "initial_sidebar_state": "expanded"
        }
        self.auth = SocialMediaAuth(
            app_id=st.secrets["facebook"]["app_id"],
            app_secret=st.secrets["facebook"]["app_secret"],
            redirect_uri='https://localhost:8502/'
        )
        self.post_history = PostHistory()

    def setup_page(self):
        """Configure the Streamlit page"""
        st.set_page_config(**self.config)

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'access_token' not in st.session_state:
            st.session_state.access_token = None
            st.session_state.page_token = None
            st.session_state.page_id = None
            st.session_state.ig_user_id = None

    def run(self):
        """Run the main application"""
        self.setup_page()
        self.initialize_session_state()
        
        st.title(self.config["page_title"])
        
        if st.session_state.access_token:
            self.show_logged_in_interface()
        else:
            self.show_login_interface()

    def show_logged_in_interface(self):
        """Show interface for logged-in users"""
        st.success("You are logged in!")
        st.write(f"Access token: {st.session_state.access_token[:10]}...")
        
        tabs = st.tabs(["Post Content", "Trending Hashtags", "Description Analysis", "Post History"])
        
        with tabs[0]:
            self.show_posting_interface()
        
        with tabs[1]:
            self.show_hashtag_interface()
        
        with tabs[2]:
            self.show_description_analysis_interface()
        
        with tabs[3]:
            self.show_history_interface()

    def show_posting_interface(self):
        """Show the content posting interface"""
        col1, col2 = st.columns(2)
        
        # Facebook posting
        with col1:
            self.show_facebook_posting()
        
        # Instagram posting
        with col2:
            self.show_instagram_posting()

    def show_facebook_posting(self):
        """Show Facebook posting interface"""
        st.subheader("Facebook Posting")
        fb_manager = FacebookManager(st.session_state.access_token)
        pages = fb_manager.get_pages()
        
        if pages:
            selected_page = st.selectbox(
                "Select Facebook Page",
                [f"{page['name']} ({page['id']})" for page in pages],
                key="fb_page_select"
            )
            selected_page_id = selected_page.split('(')[-1].strip(')')
            st.session_state.page_id = selected_page_id
            st.session_state.page_token = next(
                page['access_token'] for page in pages 
                if page['id'] == selected_page_id
            )
            
            image_url = st.text_input("Image URL for Facebook")
            message = st.text_area("Message for Facebook")
            
            if st.button("Post to Facebook"):
                self.handle_facebook_post(fb_manager, image_url, message)
        else:
            st.warning("No Facebook Pages found.")

    def show_instagram_posting(self):
        """Show Instagram posting interface"""
        st.subheader("Instagram Posting")
        ig_manager = InstagramManager(st.session_state.access_token)
        ig_accounts = ig_manager.get_accounts()
        
        if ig_accounts:
            selected_account = st.selectbox(
                "Select Instagram Account",
                [f"{account['name']} (@{account['username']})" for account in ig_accounts],
                key="ig_account_select"
            )
            selected_account_id = next(
                account['id'] for account in ig_accounts 
                if f"{account['name']} (@{account['username']})" == selected_account
            )
            st.session_state.ig_user_id = selected_account_id
            
            ig_image_url = st.text_input("Image URL for Instagram")
            ig_caption = st.text_area("Caption for Instagram")
            
            if st.button("Post to Instagram"):
                self.handle_instagram_post(ig_manager, ig_image_url, ig_caption)
        else:
            st.warning("No Instagram Business accounts found.")

    def handle_facebook_post(self, fb_manager: FacebookManager, image_url: str, message: str):
        """Handle Facebook post submission"""
        if image_url and message:
            with st.spinner("Posting to Facebook..."):
                result = fb_manager.post_content(
                    st.session_state.page_id,
                    st.session_state.page_token,
                    image_url,
                    message
                )
                if result:
                    st.success("Posted successfully to Facebook!")
                    self.post_history.add_post('Facebook', result)
        else:
            st.warning("Please fill in all Facebook fields")

    def handle_instagram_post(self, ig_manager: InstagramManager, image_url: str, caption: str):
        """Handle Instagram post submission"""
        if image_url and caption:
            with st.spinner("Posting to Instagram..."):
                result = ig_manager.post_content(
                    st.session_state.ig_user_id,
                    image_url,
                    caption
                )
                if result:
                    st.success("Posted successfully to Instagram!")
                    self.post_history.add_post('Instagram', result)
        else:
            st.warning("Please fill in all Instagram fields")

    def show_hashtag_interface(self):
        """Show the hashtag analysis interface"""
        st.subheader("Find Trending Hashtags")
        if st.session_state.ig_user_id:
            seed_hashtag = st.text_input("Enter a hashtag to find related trending tags", "#")
            if st.button("Get Trending Hashtags"):
                self.handle_hashtag_analysis(seed_hashtag)
        else:
            st.warning("Please select an Instagram account first")

    def handle_hashtag_analysis(self, seed_hashtag: str):
        """Handle hashtag analysis request"""
        if seed_hashtag:
            with st.spinner("Analyzing hashtag trends..."):
                ig_manager = InstagramManager(st.session_state.access_token)
                trending_tags = ig_manager.get_trending_hashtags(
                    st.session_state.ig_user_id,
                    seed_hashtag
                )
                if trending_tags:
                    st.success("Found trending hashtags!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Top related hashtags:")
                        for tag, count in trending_tags:
                            st.write(f"{tag}: {count} posts")
                    with col2:
                        hashtag_string = " ".join([tag for tag, _ in trending_tags])

                        st.text_area("Copy these hashtags:", hashtag_string)
                else:
                    st.warning("No trending hashtags found for this seed hashtag.")
        else:
            st.warning("Please enter a seed hashtag")

    def show_history_interface(self):
        """Show the post history interface"""
        st.subheader("Post History")
        history = self.post_history.get_history()
        if history:
            for post in reversed(history):
                with st.expander(f"{post['platform']} post - {post['timestamp']}"):
                    st.json(post['data'])
        else:
            st.info("No posts yet. Your posting history will appear here.")

    def show_login_interface(self):
        """Show the login interface for non-authenticated users"""
        st.write("Please log in to post to Facebook or Instagram.")
        col1, col2 = st.columns(2)
        with col1:
            self.show_facebook_login()
        with col2:
            self.show_instagram_login()
        
        # Handle OAuth callback
        code = st.query_params.get("code")
        if code:
            self.handle_oauth_callback(code)

    def show_facebook_login(self):
        """Show Facebook login button"""
        auth_url = self.auth.generate_auth_url('facebook')
        st.markdown(f"[Login with Facebook]({auth_url})")

    def show_instagram_login(self):
        """Show Instagram login button"""
        auth_url = self.auth.generate_auth_url('instagram')
        st.markdown(f"[Login with Instagram]({auth_url})")

    def handle_oauth_callback(self, code: str):
        """Handle OAuth callback and token generation"""
        access_token = self.auth.get_access_token(code)
        if access_token:
            st.session_state.access_token = access_token
            st.rerun()
        else:
            st.error("Failed to get access token.")

    def show_description_analysis_interface(self):
        """Show the description analysis interface"""
        st.subheader("Description Analysis & Generation")
        
        if not st.session_state.ig_user_id:
            st.warning("Please select an Instagram account first")
            return
            
        hashtag = st.text_input("Enter a hashtag to analyze top posts", "#")
        num_posts = st.slider("Number of posts to analyze", 10, 100, 50)
        
        if st.button("Analyze Descriptions"):
            if hashtag:
                with st.spinner("Analyzing top posts..."):
                    analyzer = ContentAnalyzer(st.session_state.access_token)
                    posts = analyzer.get_top_posts(
                        st.session_state.ig_user_id,
                        hashtag,
                        num_posts
                    )
                    
                    if posts:
                        analysis = analyzer.analyze_descriptions(posts)
                        template = analyzer.generate_description_template(analysis)
                        
                        # Display top performing posts
                        st.subheader("🏆 Top Performing Posts")
                        for idx, post in enumerate(analysis['top_performing_posts'], 1):
                            with st.expander(f"Top Post #{idx} - {post['engagement_score']:,} engagement score"):
                                st.markdown("**Caption:**")
                                st.text(post['caption'])
                                st.markdown(f"""
                                **Stats:**
                                - Likes: {post['likes']:,}
                                - Comments: {post['comments']:,}
                                - Total Engagement: {post['engagement_score']:,}
                                """)
                                if post['permalink']:
                                    st.markdown(f"[View Post]({post['permalink']})")
                        
                        # Display analysis results
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📊 Content Analysis")
                            st.write(f"Average caption length: {analysis['avg_length']:.0f} characters")
                            
                            st.write("Top phrases:")
                            for phrase, count in analysis['common_phrases']:
                                st.write(f"- {phrase} ({count} times)")
                            
                            st.write("\nMost used emojis:")
                            for emoji, count in analysis['emoji_usage'].items():
                                st.write(f"- {emoji}: {count} times")
                        
                        with col2:
                            st.subheader("🔍 Structure Analysis")
                            for key, value in analysis['structure_patterns'].items():
                                st.write(f"- {key.replace('_', ' ').title()}: {value:.1f}%")
                            
                            st.write("\nCommon words:")
                            for word, count in analysis['common_words']:
                                st.write(f"- {word} ({count} times)")
                        
                        st.subheader("📝 Generated Template")
                        st.text_area("Use this template as a starting point:", template, height=200)
                        
                        # Add copy buttons for top posts
                        st.subheader("Quick Copy")
                        col1, col2 = st.columns(2)
                        with col1:
                            if analysis['top_performing_posts']:
                                if st.button("Copy Top Post #1"):
                                    st.text_area("Top Post #1 Caption:", 
                                            analysis['top_performing_posts'][0]['caption'])
                        with col2:
                            if len(analysis['top_performing_posts']) > 1:
                                if st.button("Copy Top Post #2"):
                                    st.text_area("Top Post #2 Caption:", 
                                            analysis['top_performing_posts'][1]['caption'])
                    else:
                        st.warning("No posts found for this hashtag.")
            else:
                st.warning("Please enter a hashtag to analyze")

def main():
    app = SocialMediaApp()
    app.run()

if __name__ == "__main__":
    main()