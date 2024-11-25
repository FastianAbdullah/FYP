import streamlit as st

from utils.SocialMediaAuth import SocialMediaAuth
from utils.UserPostHistory import UserPostHistory
from utils.FacebookManager import FacebookManager
from utils.InstagramManager import InstagramManager
from utils.ContentAnalyzer import ContentAnalyzer



#Main StreamLit SocialMediaApp.
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
        self.post_history = UserPostHistory()

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
