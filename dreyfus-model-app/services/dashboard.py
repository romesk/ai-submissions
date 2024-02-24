from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.utils import get_user_answers
from models import Level

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


REQUIRED_POINTS = {
    1: 0,
    2: 15,
    3: 30,
    4: 50,
    5: 70
}

@dashboard_bp.route('', methods=['GET'])
@jwt_required()
def get_final_results():
    user_id = get_jwt_identity()
    user_answers = get_user_answers(user_id, range(1, 5 + 1), True)

    # calculate user points
    points = sum(map(lambda x: x.answer.points, user_answers))

    # calculate user level
    user_level = 1
    for level_id, points_required in REQUIRED_POINTS.items():
        if points >= points_required:
            user_level = level_id

    # get level name and level description
    level = Level.query.get(user_level)

    print("User points: ", points)
    
    return jsonify({
            'total_points': points,
            'user_level': user_level,
            'level_name': level.name,
            'level_description': level.description,
            'user_answers': [{
                'question_id': user_answer.answer.question_id,
                'answer_id': user_answer.answer_id,
                'content': user_answer.answer.content,
                'points': user_answer.answer.points,
                'max_points': 5
            } for user_answer in user_answers]
        }), 200