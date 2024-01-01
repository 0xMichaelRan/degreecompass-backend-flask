import zhipuai
import os
from dotenv import load_dotenv
from prompts.major_prompts import get_major_qa_prompt

load_dotenv()

class LLMService:
    def __init__(self):
        self.client = zhipuai.ZhipuAI(api_key=os.getenv('ZHIPUAI_API_KEY'))
        
    def get_major_qa(self, major_info):
        prompt = get_major_qa_prompt(major_info)
        
        response = self.client.chat.completions.create(
            model=os.getenv('ZHIPUAI_MODEL'),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        
        content = response.choices[0].message.content
        print(f"LLM Response for major {major_info['major_id']}:")
        print(content)
        
        # Validate SQL syntax
        if not all(line.strip().startswith('INSERT INTO major_qa') 
                  for line in content.strip().split('\n') if line.strip()):
            raise ValueError("Invalid SQL format in LLM response")
        
        return content

    def get_major_intro(self, major_info):
        prompt = get_major_intro_prompt(major_info)
        response = self.client.chat.completions.create(
            model=os.getenv('ZHIPUAI_MODEL'),
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content