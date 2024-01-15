from flask import Blueprint, jsonify, request
from services.major_service import MajorService
from repositories.major_repository import MajorRepository
import logging

logger = logging.getLogger(__name__)

major_bp = Blueprint('major', __name__)
major_service = MajorService(MajorRepository())

@major_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        result = major_service.get_categories()
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        page = max(int(request.args.get('page', 1)), 1)
        page_size = int(request.args.get('page_size', 28))
        category_id = request.args.get('category')
        result = major_service.get_subjects(category_id, page, page_size)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors', methods=['GET'])
def get_majors():
    try:
        page = max(int(request.args.get('page', 1)), 1)
        page_size = int(request.args.get('page_size', 28))
        category_id = request.args.get('category')
        subject_id = request.args.get('subject')
        result = major_service.get_majors(category_id, subject_id, page, page_size)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors/<major_id>', methods=['GET'])
def get_major_by_id(major_id):
    try:
        major = major_service.get_major_by_id(major_id)
        return jsonify(major), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors/<major_id>/qa', methods=['GET'])
def get_major_qa(major_id):
    try:
        qa_data = major_service.get_major_qa(major_id)
        return jsonify(qa_data), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors/<major_id>/intro', methods=['GET'])
def get_major_intro(major_id):
    try:
        major = major_service.get_major_by_id(major_id)
        intro = major_service.get_major_intro(major_id)
        return jsonify({'data': intro}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors/<major_id>/ask', methods=['POST'])
def ask_major_question(major_id):
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required'}), 400

        # Get major details and intro for context
        major = major_service.get_major_by_id(major_id)
        intro = major_service.get_major_intro(major_id)
        
        # Create context for AI
        context = {
            'major_name': major['major_name'],
            'major_id': major_id,
            'intro_content': intro
        }
        
        # Get AI response using LLM service
        answer = major_service.ask_major_question(data['question'], context)
        
        return jsonify({'answer': answer}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors/search', methods=['GET'])
def search_majors():
    try:
        keyword = request.args.get('keyword', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        logger.info(f"Searching majors with keyword: '{keyword}', page: {page}")
        result = major_service.search_majors(keyword, page, page_size)
        logger.info(f"Search completed, found {len(result['data'])} results")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in search_majors: {str(e)}")
        return jsonify({'error': str(e)}), 500