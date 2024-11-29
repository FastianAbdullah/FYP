from huggingface_hub import InferenceClient
import textwrap
import json

REPO_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def create_llm_client(repo_id: str, timeout: int = 200) -> InferenceClient:
    return InferenceClient(model=repo_id, timeout=timeout)

def call_llm(inference_client: InferenceClient, prompt: str, max_tokens: int = 400) -> str:
    response = inference_client.post(
        json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": max_tokens},
            "task": "text-generation",
        },
    )
    return json.loads(response.decode())[0]["generated_text"]

def create_text_analysis_prompt(user_text: str) -> str:
    """
    Create a more concise and direct prompt for text analysis.
    
    Args:
        user_text (str): The text to be analyzed
    
    Returns:
        str: Formatted prompt for text analysis
    """
    return f"""Analyze the following text and extract its core purpose and relevant single-word hashtags:

Text: {user_text}

Guidelines:
1. Purpose: Create a concise 15-20 word sentence capturing the primary topic and intent.
2. Hashtags: Provide 2-3 single-word, free morpheme hashtags that precisely target the content's core audience.

Format your response exactly like this:
Purpose: [Concise purpose sentence]
Hashtag: [Single-word hashtags separated by spaces]"""

def main():
    llm_client = create_llm_client(REPO_ID)
    
    example_text = "I am happy to announce i have been promoted as senior software engineer in my company, growth matters"
    
    response = call_llm(llm_client, create_text_analysis_prompt(example_text))
    
    print(textwrap.fill(text=response, width=70))

if __name__ == "__main__":
    main()