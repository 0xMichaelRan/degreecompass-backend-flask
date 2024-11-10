from flask import Blueprint, jsonify, request
from services.major_service import MajorService
from repositories.major_repository import MajorRepository

major_bp = Blueprint('major', __name__)
major_service = MajorService(MajorRepository())

@major_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        page = max(int(request.args.get('page', 1)), 1)
        page_size = min(int(request.args.get('page_size', 10)), 20)
        result = major_service.get_categories(page, page_size)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        page = max(int(request.args.get('page', 1)), 1)
        page_size = min(int(request.args.get('page_size', 10)), 20)
        category_id = request.args.get('category')
        result = major_service.get_subjects(category_id, page, page_size)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@major_bp.route('/majors', methods=['GET'])
def get_majors():
    try:
        page = max(int(request.args.get('page', 1)), 1)
        page_size = min(int(request.args.get('page_size', 10)), 20)
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