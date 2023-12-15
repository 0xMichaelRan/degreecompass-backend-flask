from flask import Blueprint, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from config.db_config import db_config

major_bp = Blueprint('major', __name__)

def get_db_connection():
    return psycopg2.connect(
        dbname=db_config['dbname'],
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port']
    )

@major_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        # Get pagination parameters
        page = max(int(request.args.get('page', 1)), 1)  # minimum page is 1
        page_size = min(int(request.args.get('page_size', 10)), 20)  # maximum size is 20
        offset = (page - 1) * page_size
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get total count
        cur.execute('SELECT COUNT(*) FROM categories')
        total_count = cur.fetchone()['count']
        
        # Get paginated data
        cur.execute('''
            SELECT * FROM categories 
            ORDER BY category_id 
            LIMIT %s OFFSET %s
        ''', (page_size, offset))
        categories = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'data': categories,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        # Get pagination parameters
        page = max(int(request.args.get('page', 1)), 1)
        page_size = min(int(request.args.get('page_size', 10)), 20)
        offset = (page - 1) * page_size
        
        # Get category parameter
        category_id = request.args.get('category')
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get total count
        if category_id:
            cur.execute('SELECT COUNT(*) FROM subjects WHERE category_id = %s', (category_id,))
        else:
            cur.execute('SELECT COUNT(*) FROM subjects')
        total_count = cur.fetchone()['count']
        
        # Get paginated data
        if category_id:
            cur.execute('''
                SELECT s.*, c.category_name 
                FROM subjects s 
                JOIN categories c ON s.category_id = c.category_id 
                WHERE s.category_id = %s
                ORDER BY s.subject_id
                LIMIT %s OFFSET %s
            ''', (category_id, page_size, offset))
        else:
            cur.execute('''
                SELECT s.*, c.category_name 
                FROM subjects s 
                JOIN categories c ON s.category_id = c.category_id 
                ORDER BY s.subject_id
                LIMIT %s OFFSET %s
            ''', (page_size, offset))
            
        subjects = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify({
            'data': subjects,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors', methods=['GET'])
def get_majors():
    try:
        # Get pagination parameters
        page = max(int(request.args.get('page', 1)), 1)
        page_size = min(int(request.args.get('page_size', 10)), 20)
        offset = (page - 1) * page_size
        
        # Get filter parameters
        category_id = request.args.get('category')
        subject_id = request.args.get('subject')
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get total count based on filters
        if subject_id:
            cur.execute('SELECT COUNT(*) FROM majors WHERE subject_id = %s', (subject_id,))
        elif category_id:
            cur.execute('''
                SELECT COUNT(*) FROM majors m
                JOIN subjects s ON m.subject_id = s.subject_id
                WHERE s.category_id = %s
            ''', (category_id,))
        else:
            cur.execute('SELECT COUNT(*) FROM majors')
        total_count = cur.fetchone()['count']
        
        # Get paginated data
        if subject_id:
            cur.execute('''
                SELECT m.*, s.subject_name, c.category_name 
                FROM majors m
                JOIN subjects s ON m.subject_id = s.subject_id
                JOIN categories c ON s.category_id = c.category_id
                WHERE m.subject_id = %s
                ORDER BY m.major_id
                LIMIT %s OFFSET %s
            ''', (subject_id, page_size, offset))
        elif category_id:
            cur.execute('''
                SELECT m.*, s.subject_name, c.category_name 
                FROM majors m
                JOIN subjects s ON m.subject_id = s.subject_id
                JOIN categories c ON s.category_id = c.category_id
                WHERE c.category_id = %s
                ORDER BY m.major_id
                LIMIT %s OFFSET %s
            ''', (category_id, page_size, offset))
        else:
            cur.execute('''
                SELECT m.*, s.subject_name, c.category_name 
                FROM majors m
                JOIN subjects s ON m.subject_id = s.subject_id
                JOIN categories c ON s.category_id = c.category_id
                ORDER BY m.major_id
                LIMIT %s OFFSET %s
            ''', (page_size, offset))
            
        majors = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify({
            'data': majors,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors/<major_id>', methods=['GET'])
def get_major_by_id(major_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('''
            SELECT m.*, s.subject_name, c.category_name 
            FROM majors m
            JOIN subjects s ON m.subject_id = s.subject_id
            JOIN categories c ON s.category_id = c.category_id
            WHERE m.major_id = %s
        ''', (major_id,))
        
        major = cur.fetchone()
        cur.close()
        conn.close()
        
        if major is None:
            return jsonify({'error': 'Major not found'}), 404
            
        return jsonify(major), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500