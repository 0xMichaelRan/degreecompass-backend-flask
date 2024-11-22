from services.llm_service import LLMService

class MajorService:
    def __init__(self, repository):
        self.repository = repository
        self.llm_service = LLMService()

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
        # First check if we have cached QA
        qa_data = self.repository.get_major_qa(major_id)
        
        if qa_data:
            return qa_data
            
        # If no cached data, get major info and generate QA
        major_info = self.repository.get_major_by_id(major_id)
        if not major_info:
            raise ValueError('Major not found')
            
        # Generate QA using LLM
        qa_content = self.llm_service.get_major_qa(major_info)
        
        # Save and return the QA content
        return self.repository.save_major_qa(major_id, qa_content)
  