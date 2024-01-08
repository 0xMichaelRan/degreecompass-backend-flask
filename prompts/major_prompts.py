def get_major_intro_prompt(major_info):
    return f"""
    我是一名大学申请者，对大学专业不太了解。请用书面语，并以适当的Markdown格式为我提供关于【{major_info['major_name']}】的一般信息，包括以下几个方面：

    学习领域：该专业涉及的主要学习领域是什么？

    适合学生类型：【{major_info['major_name']}】适合什么类型的学生？例如，具备哪些特质或兴趣的学生可能更适合这个专业？

    就业机会：学习【{major_info['major_name']}】的学生在毕业后有哪些常见的就业方向和职业机会？行业前景如何？

    高校选择：哪些著名高校的这个专业比较著名？有哪些知名校友？

    不要提到“前景广阔”，“发展空间较大”之类的词语，用中肯的语气，偏年轻化的语言，控制总字数在200字以内，不需要标题，不要用列表形式。
    """ 

def get_major_qa_prompt(major_info):
    return f"""
    请你作为一个专业的教育顾问，为以下专业提供详细的问答信息，并以SQL INSERT语句的形式返回：

    专业名称：{major_info['major_name']}
    学科类别：{major_info['subject_name']}
    门类：{major_info['category_name']}

    请为以下5个问题提供答案，并将答案转换为对应的SQL INSERT语句：
    1. {major_info['major_name']}主要学什么？
    2. 哪些大学课程是{major_info['major_name']}的本科学生必修的？
    3. 未来就业方向有哪些？有哪些著名企业定向招聘？
    4. 读{major_info['major_name']}的学生考研比例大吗？
    5. 读{major_info['major_name']}的学生适合做公务员吗？

    请严格按照以下格式返回SQL语句（每个INSERT必须在单独一行）：
    INSERT INTO major_qa (major_id, question, answer) VALUES ('{major_info['major_id']}', '这个专业主要学什么？', '答案1');
    INSERT INTO major_qa (major_id, question, answer) VALUES ('{major_info['major_id']}', '这个专业的主要课程有哪些？', '答案2');

    注意：
    1. 每个INSERT语句必须单独一行
    2. 答案中如有单引号需要用两个单引号转义
    3. 每个答案控制在100-200字之间
    4. 不要包含markdown格式或其他额外内容
    """

def get_major_ask_prompt(context, question):
    return f"""
    我是一名大学申请者，对【{context['major_name']}】专业有一些疑问。请根据以下背景信息回答我的问题：

    专业介绍：
    {context['intro_content']}

    我的问题是：{question}

    请提供准确且有帮助的回答。如果问题无法完全根据提供的背景信息回答，请说明这一点，并提供与该专业相关的一般性指导。请用中肯的语气，偏年轻化的语言回答，控制在100字以内。不要使用"前景广阔"，"发展空间较大"之类的词语。
    """