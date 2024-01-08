from services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

class MajorService:
    def __init__(self, repository):
        self.repository = repository
        self.llm_service = LLMService()
        logger.info("MajorService initialized")

    def get_paginated_response(self, items, count, page, page_size):
        return {
            'data': items,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': count,
                'total_pages': (count + page_size - 1) // page_size
            }
        }

    def get_categories(self):
        return self.repository.get_categories()

    def get_subjects(self, category_id, page, page_size):
        offset = (page - 1) * page_size
        subjects, count = self.repository.get_subjects(category_id, page_size, offset)
        return self.get_paginated_response(subjects, count, page, page_size)

    def get_majors(self, category_id, subject_id, page, page_size):
        offset = (page - 1) * page_size
        majors, count = self.repository.get_majors(category_id, subject_id, page_size, offset)
        return self.get_paginated_response(majors, count, page, page_size)

    def get_major_by_id(self, major_id):
        major = self.repository.get_major_by_id(major_id)
        if not major:
            raise ValueError('Major not found')
        return major

    def get_major_qa(self, major_id):
        logger.info(f"Getting QA data for major {major_id}")
        
        # First check if we have cached QA
        qa_data = self.repository.get_major_qa(major_id)
        
        if qa_data:
            logger.info(f"Found cached QA data for major {major_id}")
            return qa_data
            
        logger.info(f"No cached QA found for major {major_id}, generating new content")
        
        # If no cached data, get major info and generate QA
        major_info = self.repository.get_major_by_id(major_id)
        if not major_info:
            logger.error(f"Major not found: {major_id}")
            raise ValueError('Major not found')
            
        # Generate QA using LLM
        qa_content = self.llm_service.get_major_qa(major_info)
        
        # Save and return the QA content
        return self.repository.save_major_qa(major_id, qa_content)

    def get_major_intro(self, major_id):
        logger.info(f"Getting intro data for major {major_id}")
        
        # First check if we have cached intro
        intro_data = self.repository.get_major_intro(major_id)
        
        if intro_data:
            logger.info(f"Found cached intro data for major {major_id}")
            return intro_data
            
        logger.info(f"No cached intro found for major {major_id}, generating new content")
        
        # If no cached data, get major info and generate intro
        major_info = self.repository.get_major_by_id(major_id)
        if not major_info:
            logger.error(f"Major not found: {major_id}")
            raise ValueError('Major not found')
            
        # Generate intro using LLM
        intro_content = self.llm_service.get_major_intro(major_info)
        
        # Save and return the intro content
        return self.repository.save_major_intro(major_id, intro_content)

    def ask_major_question(self, question, context):
        logger.info(f"Processing question for major {context['major_name']} (ID: {context['major_id']})")
        logger.debug(f"Question: {question}")
        
        try:
            answer = self.llm_service.ask_major_question(question, context)
            logger.info(f"Successfully got answer for major {context['major_name']}")
            return answer
        except Exception as e:
            logger.error(f"Error getting AI answer for major {context['major_name']} (ID: {context['major_id']}): {str(e)}")
            raise

    def search_majors(self, keyword, page, page_size):
        logger.info(f"Searching majors with keyword: '{keyword}', page: {page}, page_size: {page_size}")
        offset = (page - 1) * page_size
        majors, count = self.repository.search_majors(keyword, page_size, offset)
        logger.info(f"Found {count} majors matching '{keyword}'")
        return self.get_paginated_response(majors, count, page, page_size)
  