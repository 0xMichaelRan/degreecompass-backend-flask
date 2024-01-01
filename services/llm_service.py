import zhipuai
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.client = zhipuai.ZhipuAI(api_key=os.getenv('ZHIPUAI_API_KEY'))
        
    def get_major_qa(self, major_info):
        prompt = f"""
        请你作为一个专业的教育顾问，为以下专业提供详细的问答信息，并以SQL INSERT语句的形式返回：

        专业名称：{major_info['major_name']}
        学科类别：{major_info['subject_name']}
        门类：{major_info['category_name']}

        请为以下5个问题提供答案，并将答案转换为对应的SQL INSERT语句：
        1. 这个专业主要学什么？
        2. 这个专业的主要课程有哪些？
        3. 这个专业的就业方向有哪些？
        4. 这个专业需要什么特质或能力？
        5. 这个专业的发展前景如何？

        请严格按照以下格式返回SQL语句（每个INSERT必须在单独一行）：
        INSERT INTO major_qa (major_id, question, answer) VALUES ('{major_info['major_id']}', '这个专业主要学什么？', '答案1');
        INSERT INTO major_qa (major_id, question, answer) VALUES ('{major_info['major_id']}', '这个专业的主要课程有哪些？', '答案2');

        注意：
        1. 每个INSERT语句必须单独一行
        2. 答案中如有单引号需要用两个单引号转义
        3. 每个答案控制在100-200字之间
        4. 不要包含markdown格式或其他额外内容
        """

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