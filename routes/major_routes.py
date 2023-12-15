from flask import Blueprint, jsonify
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
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM categories ORDER BY category_id')
        categories = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('''
            SELECT s.*, c.category_name 
            FROM subjects s 
            JOIN categories c ON s.category_id = c.category_id 
            ORDER BY s.subject_id
        ''')
        subjects = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(subjects), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors', methods=['GET'])
def get_majors():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('''
            SELECT m.*, s.subject_name, c.category_name 
            FROM majors m
            JOIN subjects s ON m.subject_id = s.subject_id
            JOIN categories c ON s.category_id = c.category_id
            ORDER BY m.major_id
        ''')
        majors = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(majors), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 