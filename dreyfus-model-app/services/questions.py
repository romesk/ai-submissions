from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import Level, Question, Answer, db

questions_bp = Blueprint('questions', __name__, url_prefix='/polls')

@questions_bp.route('/questions', methods=['GET'])
@jwt_required() 
def get_questions():
    level_id = request.args.get('level_id', 1)
    
    if not level_id:
        return jsonify({'message': 'Level ID is required'}), 400
    
    level = Level.query.get(level_id)
    
    if not level:
        return jsonify({'message': 'Level not found'}), 404
    
    questions = Question.query.filter_by(level_id=level_id).all()
    
    questions_list = []
    for question in questions:
        answers = Answer.query.filter_by(question_id=question.id).all()
        answers_list = [{'answer_id': answer.id, 'content': answer.content, 'points': answer.points} for answer in answers]
        questions_list.append({
            'question_content': question.content,
            'question_id': question.id,
            'answers': answers_list
        })
    
    response = {
        'level_name': level.name,
        'questions': questions_list
    }
    
    return jsonify(response), 200