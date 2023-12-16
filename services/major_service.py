class MajorService:
    def __init__(self, repository):
        self.repository = repository

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

    def get_categories(self, page, page_size):
        offset = (page - 1) * page_size
        categories, count = self.repository.get_categories(page_size, offset)
        return self.get_paginated_response(categories, count, page, page_size)

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