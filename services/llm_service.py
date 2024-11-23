import zhipuai
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.client = zhipuai.ZhipuAI(api_key=os.getenv('ZHIPUAI_API_KEY'))
        
    def get_major_qa(self, major_info):
        prompt = f"""
        请你作为一个专业的教育顾问，为以下专业提供详细的问答信息：

        专业名称：{major_info['major_name']}
        学科类别：{major_info['subject_name']}
        门类：{major_info['category_name']}

        请提供以下方面的信息：
        1. 这个专业主要学什么？
        2. 这个专业的主要课程有哪些？
        3. 这个专业的就业方向有哪些？
        4. 这个专业需要什么特质或能力？
        5. 这个专业的发展前景如何？

        请确保您的回答采用正式的书面表达方式并使用合适的Markdown格式。谢谢。
        """

        response = self.client.chat.completions.create(
            model=os.getenv('ZHIPUAI_MODEL'),
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content

    def get_major_intro(self, major_info):
        prompt = f"""
        我是一名大学申请者，对大学专业不太了解。请用书面语，并以适当的Markdown格式为我提供关于【{major_info['major_name']}】的一般信息，包括以下几个方面：

        学习领域：该专业涉及的主要学习领域是什么？

        适合学生类型：【{major_info['major_name']}】适合什么类型的学生？例如，具备哪些特质或兴趣的学生可能更适合这个专业？

        就业机会：学习【{major_info['major_name']}】的学生在毕业后有哪些常见的就业方向和职业机会？

        入学要求：申请学习【{major_info['major_name']}】通常需要满足哪些学术和非学术的入学要求？

        预期薪资：在【{major_info['major_name']}】领域工作的毕业生一般可以期待怎样的起薪和职业发展薪资水平？

        请确保您的回答采用正式的书面表达方式并使用合适的Markdown格式。谢谢。
        """

        response = self.client.chat.completions.create(
            model=os.getenv('ZHIPUAI_MODEL'),
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content