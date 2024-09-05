import os,torch
from transformers import AutoTokenizer,AutoModelForCausalLM
import huggingface_hub
from dotenv import load_dotenv

load_dotenv(dotenv_path="D:\Study\FYP\.env")
hf_llama_guard_tk = os.getenv(key="HF_LLAMA_GUARD")

class GuardRail:

    def __init__(self,
                 model_name : str,
                 access_token:str):
        
        self.access_token = access_token
        self.model_id = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float32
    
    def setup_model_n_tokenizer(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id,torch_dtype = self.dtype,device_map = self.device)

        return None
    
    def read_unsafe_categories(self) -> str:
        with open(file="utils\unsafe_categories.txt",mode="r") as f:
            unsafe_categories = f.read()

        return unsafe_categories
    
    def moderate_prompt_for_chat(self,chat):

        conversation = [turn["content"] for turn in chat]
        role = "Agent" if len(conversation) % 2 == 0 else "User"

        # PROMPT TEMPLATE FROM LLAMA_GUARD PAPER
        # SEE LLAMA_GUARD_PAPER_REF IN IMAGES FOR REFERENCE
        prompt = f"""[INST] Task: Check if there is unsafe content in '{role}' messages in conversations according our safety policy with the below categories.

    <BEGIN UNSAFE CONTENT CATEGORIES>
    {self.read_unsafe_categories()}
    <END UNSAFE CONTENT CATEGORIES>

    <BEGIN CONVERSATION>

    """

        # Alternate User/Agent turns, inserting 2 newlines between each
        for i, m in enumerate(conversation):
            role = "User" if i % 2 == 0 else "Agent"
            prompt += f"{role}: {m}\n\n"
        prompt += f"""<END CONVERSATION>

    Provide your safety assessment for {role} in the above conversation:
    - A Single line which either read 'safe' or 'unsafe'.[/INST]"""
        return prompt

    def moderate_custom_chat(self,chat):
        prompt = self.moderate_prompt_for_chat(chat)
        input_ids = self.tokenizer.apply_chat_template(prompt,return_tensors="pt").to(self.device)
        output = self.model.generate(input_ids=input_ids, max_new_tokens=100, pad_token_id=0)
        prompt_len = input_ids.shape[-1]

        return self.tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True)

    def sanitize_input(self,
                       user_description : str) -> str:
        
        self.user_content = user_description
        chat_template = [
            {'role':'User' , 'content':f"{user_description}"}
        ]
        result = self.moderate_custom_chat(chat=chat_template)
        
        return result

    def sanitize_output(self,
                        initial_description : str,
                        llm_response : str):
        
        chat_template = [
            {'role':'User','content':f"{initial_description}"},
            {'role':'assistant','content':f"{llm_response}"}
        ]

        result = self.moderate_custom_chat(chat=chat_template)
        return result
        

# huggingface_hub.login(token=hf_llama_guard_tk)

# with open(file="utils\unsafe_categories.txt",mode="r") as f:
#     unsafe_categories = f.read()

# model_id = "meta-llama/LlamaGuard-7b"
# device = "cpu"
# dtype = torch.float32

# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForCausalLM.from_pretrained(model_id,torch_dtype=dtype,device_map=device)

# def moderate(chat):
#     input_ids = tokenizer.apply_chat_template(chat, return_tensors="pt").to(device)
#     output = model.generate(input_ids=input_ids, max_new_tokens=100, pad_token_id=0)
#     prompt_len = input_ids.shape[-1]
#     return tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True)

# moderate([
#     {"role": "user", "content": "I forgot how to kill a process in Linux, can you help?"},
#     {"role": "assistant", "content": "Sure! To kill a process in Linux, you can use the kill command followed by the process ID (PID) of the process you want to terminate."},
# ])
# # `safe`
