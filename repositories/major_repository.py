from services.db_service import DatabaseService

class MajorRepository:
    @staticmethod
    def get_categories():
        return DatabaseService.execute_query(
            'SELECT * FROM categories ORDER BY category_id'
        )

    @staticmethod
    def get_subjects(category_id, page_size, offset):
        count_query = 'SELECT COUNT(*) FROM subjects'
        count_params = None
        
        if category_id:
            count_query += ' WHERE category_id = %s'
            count_params = (category_id,)
        
        count = DatabaseService.execute_single_query(count_query, count_params)['count']
        
        query = '''
            SELECT s.*, c.category_name 
            FROM subjects s 
            JOIN categories c ON s.category_id = c.category_id 
        '''
        
        params = []
        if category_id:
            query += ' WHERE s.category_id = %s'
            params.append(category_id)
        
        query += ' ORDER BY s.subject_id LIMIT %s OFFSET %s'
        params.extend([page_size, offset])
        
        subjects = DatabaseService.execute_query(query, tuple(params))
        return subjects, count

    @staticmethod
    def get_majors(category_id, subject_id, page_size, offset):
        # Build count query based on filters
        count_query = 'SELECT COUNT(*) FROM majors m'
        count_params = []
        
        if subject_id:
            count_query += ' WHERE subject_id = %s'
            count_params.append(subject_id)
        elif category_id:
            count_query += ' JOIN subjects s ON m.subject_id = s.subject_id WHERE s.category_id = %s'
            count_params.append(category_id)
            
        count = DatabaseService.execute_single_query(count_query, tuple(count_params))['count']
        
        # Build data query
        query = '''
            SELECT m.*, s.subject_name, c.category_name 
            FROM majors m
            JOIN subjects s ON m.subject_id = s.subject_id
            JOIN categories c ON s.category_id = c.category_id
        '''
        
        params = []
        if subject_id:
            query += ' WHERE m.subject_id = %s'
            params.append(subject_id)
        elif category_id:
            query += ' WHERE c.category_id = %s'
            params.append(category_id)
            
        query += ' ORDER BY m.major_id LIMIT %s OFFSET %s'
        params.extend([page_size, offset])
        
        majors = DatabaseService.execute_query(query, tuple(params))
        return majors, count

    @staticmethod
    def get_major_by_id(major_id):
        return DatabaseService.execute_single_query(
            '''
            SELECT m.*, s.subject_name, c.category_name 
            FROM majors m
            JOIN subjects s ON m.subject_id = s.subject_id
            JOIN categories c ON s.category_id = c.category_id
            WHERE m.major_id = %s
            ''',
            (major_id,)
        ) 