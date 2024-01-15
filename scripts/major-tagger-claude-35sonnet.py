import json
import time
import zhipuai
from typing import List, Dict
import pandas as pd
from tqdm import tqdm

# Initialize Zhipu AI client
zhipuai.api_key = "YOUR_API_KEY"

class MajorTagger:
    def __init__(self):
        self.tag_categories = {
            "职业发展": {
                "薪资水平": "描述专业毕业生的薪资范围和发展",
                "工作强度": "工作压力和时间投入程度",
                "工作环境": "典型的工作场所和条件",
                "职业道路": "可能的职业发展路径"
            },
            "就业方向": {
                "热门城市": "最适合发展的城市",
                "主要行业": "主要就业的行业领域",
                "典型职位": "常见的就业岗位"
            },
            "能力培养": {
                "硬实力": "专业相关的技术能力",
                "软实力": "通用职场能力",
                "特殊技能": "该专业特有的能力"
            },
            "学习特点": {
                "核心课程": "主要专业课程",
                "课程难度": "学习难度和特点",
                "学习方式": "主要的学习形式"
            },
            "基础数据": {
                "男女比例": "专业性别分布情况",
                "高中相关学科": "需要重点关注的高中学科",
                "选考建议": "高考选科建议"
            },
            "社会议题": {
                "刻板印象": "社会对该专业的固有印象",
                "社会争议": "该专业相关的社会热点话题",
                "职场现状": "真实的职场情况"
            }
        }
        
    def generate_prompt(self, major_info: Dict) -> str:
        """Generate prompt for Zhipu AI"""
        prompt = f"""请你作为教育专家，为以下专业生成详细的标签信息：

专业名称：{major_info['major_name']}
所属学科：{major_info['subject_name']}
所属门类：{major_info['category_name']}

请为这个专业生成如下类别的标签，每个子类别生成3-5个具体的标签：

{json.dumps(self.tag_categories, ensure_ascii=False, indent=2)}

请用JSON格式返回，确保每个类别都有具体的标签。每个标签应该简洁明了，4-10个字为宜。
请确保返回格式完全符合示例格式，便于解析。不要包含任何其他说明文字。"""

        return prompt

    def call_zhipu_api(self, prompt: str, max_retries: int = 3) -> Dict:
        """Call Zhipu AI API with retry mechanism"""
        for attempt in range(max_retries):
            try:
                response = zhipuai.model_api.invoke(
                    model="chatglm_pro",
                    prompt=prompt,
                    top_p=0.7,
                    temperature=0.7,
                    request_timeout=60
                )
                
                if response.get('code') == 200:
                    return json.loads(response['data']['choices'][0]['content'])
                
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
        
        return {}

    def process_majors(self, input_file: str, output_file: str, batch_size: int = 10):
        """Process all majors in batches"""
        # Read input data
        with open(input_file, 'r', encoding='utf-8') as f:
            major_data = json.load(f)['data']
        
        # Initialize results storage
        results = []
        
        # Process in batches with progress bar
        for i in tqdm(range(0, len(major_data), batch_size)):
            batch = major_data[i:i + batch_size]
            
            for major_info in batch:
                try:
                    prompt = self.generate_prompt(major_info)
                    tags = self.call_zhipu_api(prompt)
                    
                    # Store results
                    results.append({
                        'major_id': major_info['major_id'],
                        'major_name': major_info['major_name'],
                        'subject_name': major_info['subject_name'],
                        'category_name': major_info['category_name'],
                        'tags': tags
                    })
                    
                    # Save intermediate results
                    if len(results) % 50 == 0:
                        self.save_results(results, output_file)
                        
                except Exception as e:
                    print(f"Error processing {major_info['major_name']}: {str(e)}")
                    
                # Rate limiting
                time.sleep(1)
        
        # Save final results
        self.save_results(results, output_file)
        
        # Generate summary report
        self.generate_report(results, output_file.replace('.json', '_report.xlsx'))

    def save_results(self, results: List[Dict], output_file: str):
        """Save results to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_majors': len(results),
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
                'data': results
            }, f, ensure_ascii=False, indent=2)

    def generate_report(self, results: List[Dict], output_file: str):
        """Generate summary report in Excel"""
        summary_data = []
        
        for result in results:
            # Flatten the nested structure for easier analysis
            row = {
                'major_id': result['major_id'],
                'major_name': result['major_name'],
                'subject_name': result['subject_name'],
                'category_name': result['category_name']
            }
            
            # Add all tags as columns
            for category, subcategories in result['tags'].items():
                for subcategory, tags in subcategories.items():
                    row[f'{category}_{subcategory}'] = ' | '.join(tags)
            
            summary_data.append(row)
        
        # Create DataFrame and save to Excel
        df = pd.DataFrame(summary_data)
        df.to_excel(output_file, index=False)

def main():
    # Initialize tagger
    tagger = MajorTagger()
    
    # Process majors
    tagger.process_majors(
        input_file='majors_input.json',
        output_file='majors_tagged.json'
    )

if __name__ == "__main__":
    main()
