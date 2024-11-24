import zhipuai
import os
import logging
from dotenv import load_dotenv
from prompts.major_prompts import *

load_dotenv()
logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.client = zhipuai.ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))

    def get_major_qa(self, major_info):
        major_id = major_info["major_id"]
        logger.info(f"\n=== Sending QA request to ZhipuAI for major {major_id} ===")

        prompt = get_major_qa_prompt(major_info)

        try:
            response = self.client.chat.completions.create(
                model=os.getenv("ZHIPUAI_MODEL"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            content = response.choices[0].message.content
            logger.info(
                f"\n=== Received QA response from ZhipuAI for major {major_id} ==="
            )
            logger.debug(f"Response content: {content}")

            # Validate SQL syntax
            if not all(
                line.strip().startswith("INSERT INTO major_qa")
                for line in content.strip().split("\n")
                if line.strip()
            ):
                logger.error(f"Invalid SQL format in LLM response for major {major_id}")
                raise ValueError("Invalid SQL format in LLM response")

            return content

        except Exception as e:
            logger.error(
                f"\n=== Error calling ZhipuAI for major {major_id}: {str(e)} ==="
            )
            raise

    def get_major_intro(self, major_info):
        prompt = get_major_intro_prompt(major_info)

        logger.info(
            f"\n=== Sending intro request to ZhipuAI for major {major_info['major_id']} ==="
        )

        try:
            response = self.client.chat.completions.create(
                model=os.getenv("ZHIPUAI_MODEL"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            content = response.choices[0].message.content
            logger.info(
                f"\n=== Received intro response from ZhipuAI for major {major_info['major_id']} ==="
            )
            logger.debug(f"Response content: {content}")

            return content

        except Exception as e:
            logger.error(
                f"\n=== Error calling ZhipuAI for major {major_info['major_id']}: {str(e)} ==="
            )
            raise

    def ask_major_question(self, question, context):
        try:
            prompt = get_major_ask_prompt(context, question)

            logger.info(f"\n=== Sending question to ZhipuAI for major {context['major_id']} ===")

            response = self.client.chat.completions.create(
                model=os.getenv("ZHIPUAI_MODEL"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            content = response.choices[0].message.content
            logger.info(f"\n=== Received answer from ZhipuAI for major {context['major_id']} ===")
            logger.debug(f"Response content: {content}")

            return content

        except Exception as e:
            logger.error(f"\n=== Error calling ZhipuAI for major {context['major_id']}: {str(e)} ===")
            raise
