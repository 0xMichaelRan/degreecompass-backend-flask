def get_major_qa_prompt(major_info):
    return f"""
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

def get_major_intro_prompt(major_info):
    return f"""
    我是一名大学申请者，对大学专业不太了解。请用书面语，并以适当的Markdown格式为我提供关于【{major_info['major_name']}】的一般信息，包括以下几个方面：

    学习领域：该专业涉及的主要学习领域是什么？

    适合学生类型：【{major_info['major_name']}】适合什么类型的学生？例如，具备哪些特质或兴趣的学生可能更适合这个专业？

    就业机会：学习【{major_info['major_name']}】的学生在毕业后有哪些常见的就业方向和职业机会？

    控制总字数在200字以内，不需要标题，不要用列表形式。谢谢。
    """ 