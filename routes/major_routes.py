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
        # Get limit parameter, default to 10, max 20
        limit = min(int(request.args.get('limit', 10)), 20)
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM categories ORDER BY category_id LIMIT %s', (limit,))
        categories = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        # Get limit parameter, default to 10, max 20
        limit = min(int(request.args.get('limit', 10)), 20)
        # Get category parameter
        category_id = request.args.get('category')
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        if category_id:
            cur.execute('''
                SELECT s.*, c.category_name 
                FROM subjects s 
                JOIN categories c ON s.category_id = c.category_id 
                WHERE s.category_id = %s
                ORDER BY s.subject_id
                LIMIT %s
            ''', (category_id, limit))
        else:
            cur.execute('''
                SELECT s.*, c.category_name 
                FROM subjects s 
                JOIN categories c ON s.category_id = c.category_id 
                ORDER BY s.subject_id
                LIMIT %s
            ''', (limit,))
            
        subjects = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(subjects), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors', methods=['GET'])
def get_majors():
    try:
        # Get limit parameter, default to 10, max 20
        limit = min(int(request.args.get('limit', 10)), 20)
        # Get filter parameters
        category_id = request.args.get('category')
        subject_id = request.args.get('subject')
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        if subject_id:
            cur.execute('''
                SELECT m.*, s.subject_name, c.category_name 
                FROM majors m
                JOIN subjects s ON m.subject_id = s.subject_id
                JOIN categories c ON s.category_id = c.category_id
                WHERE m.subject_id = %s
                ORDER BY m.major_id
                LIMIT %s
            ''', (subject_id, limit))
        elif category_id:
            cur.execute('''
                SELECT m.*, s.subject_name, c.category_name 
                FROM majors m
                JOIN subjects s ON m.subject_id = s.subject_id
                JOIN categories c ON s.category_id = c.category_id
                WHERE c.category_id = %s
                ORDER BY m.major_id
                LIMIT %s
            ''', (category_id, limit))
        else:
            cur.execute('''
                SELECT m.*, s.subject_name, c.category_name 
                FROM majors m
                JOIN subjects s ON m.subject_id = s.subject_id
                JOIN categories c ON s.category_id = c.category_id
                ORDER BY m.major_id
                LIMIT %s
            ''', (limit,))
            
        majors = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(majors), 200
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