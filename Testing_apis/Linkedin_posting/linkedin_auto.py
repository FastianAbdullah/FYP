import requests,json,os
from dotenv import load_dotenv

load_dotenv()

class Linkedin_auto:
    def __init__(self,access_token,text,description=None,url=None) -> None:
        self.access_token=access_token
        self.headers = {
            'Authorization' : f'Bearer {self.access_token}'
        }
        self.text = text
        self.description = description
        self.url = url

    def get_user_id(self):
        url = 'https://api.linkedin.com/v2/userinfo'
        response = requests.request('GET',url=url,headers=self.headers)
        jsonData = json.loads(response.text)
        print(f'User ID: {jsonData}')
        return jsonData["sub"]

    def api_call_json(self,user_id):
        payload = {
            "author": f"urn:li:person:{user_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": f'{self.text}'
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        return json.dumps(payload)
    
    def feed_post(self,user_id):
        url = "https://api.linkedin.com/v2/ugcPosts"
        payload = self.api_call_json(user_id=user_id)

        return requests.request('POST',url,headers=self.headers,data=payload)
    
    def main_func(self):
        user_id = self.get_user_id()
        feed_post = self.feed_post(user_id=user_id)
        print(feed_post)

        return None

if __name__ == '__main__':
    access_tk = os.getenv(key="LK_ACCESS_TK")
    text = "Bro Auto Posting"
    post_maker = Linkedin_auto(access_token=access_tk,text=text)
    post_maker.main_func()

