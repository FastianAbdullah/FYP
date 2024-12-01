import requests
from typing import Dict, Optional, List

class MixtralClient:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def _format_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Format messages according to Mixtral's instruction format"""
        prompt = "<s>"
        for i, message in enumerate(messages):
            if message['role'] == 'user':
                prompt += f" [INST] {message['content']} [/INST]"
            else:
                prompt += f" {message['content']}"
            if i < len(messages) - 1 and messages[i + 1]['role'] == 'user':
                prompt += "</s>"
        print(prompt)
        return prompt

    def generate_response(self, 
                         messages: List[Dict[str, str]], 
                         max_length: int = 500, 
                         temperature: float = 0.7, 
                         top_p: float = 0.95) -> Dict:
        """Generate a response from Mixtral model"""
        formatted_prompt = self._format_prompt(messages)
        
        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_length": max_length,
                "temperature": temperature,
                "top_p": top_p,
                "return_full_text": False
            }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        
    def extract_purpose_and_hashtags(self, user_text: str) -> Optional[Dict]:
        messages = [
            {
                "role": "user",
                "content": f"""Distill the core purpose of this text in one concise sentence:
                    - Focus on the primary topic and main intent
                    - Be clear and specific
                    - Capture the essence in 15-20 words

                    Provide 2-3 strategic hashtags that precisely target the content's core audience.
                    - Hashtags should be 1-2 words each
                    - Use commonly recognized terms and avoid long phrases
                    - Ensure each hashtag is relevant and impactful

                    Text to analyze: {user_text}

                    IMPORTANT: Respond ONLY in this exact format:
                    Purpose: [Your concise purpose sentence]
                    Hashtag: [Your strategic hashtags]"""
                }
            ]
        
        try:
            response = self.generate_response(messages, max_length=150, temperature=0.7)
            
            if isinstance(response, list) and response:
                generated_text = response[0].get('generated_text', '').strip()
                return generated_text
            
            return None
        except Exception as e:
            print(f"Error extracting purpose and hashtags: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    API_TOKEN = "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"
    client = MixtralClient(API_TOKEN)
    
  
    test_text = "I am happy to announce i have been promoted as senior software engineer in my company, growth matters"
    
    result = client.extract_purpose_and_hashtags(test_text)
    
    print("Analysis Result:")
    print(result)