from flask import Blueprint, jsonify, request, g
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.utils import validate_answers, get_user_answers
from models import Level, Question, Answer, UserAnswer, db

answers_bp = Blueprint('answers', __name__, url_prefix='/answers')

@answers_bp.route('', methods=['POST'])
@jwt_required()
def send_results():
    data = request.get_json()
    user_id = get_jwt_identity()
    answers = data.get('answers', [])

    if not validate_answers(answers):
        return jsonify({'message': 'Invalid answers'}), 400

    # delete previous answers for this level id
    question_id = Answer.query.get(answers[0]).question_id
    level_id = Question.query.get(question_id).level_id
    answers_to_delete = UserAnswer.query \
        .filter_by(user_id=user_id, is_submitted=False) \
        .join(Answer, UserAnswer.answer_id == Answer.id) \
        .join(Question, Answer.question_id == Question.id) \
        .filter(Question.level_id == level_id) \
        .all()

    for answer in answers_to_delete:
        db.session.delete(answer)

    for answer_id in answers:
        user_answer = UserAnswer(
            user_id=user_id,
            answer_id=answer_id,
            is_submitted=False
        )
        db.session.add(user_answer)

    db.session.commit()
    return jsonify({'message': 'Answers sent successfully'}), 201


@answers_bp.route('', methods=['GET'])
@jwt_required()
def get_not_submitted():
    try:
        level_id = int(request.args.get('level_id', 1))
    except ValueError:
        return jsonify({'message': 'Invalid level ID'}), 400
    
    is_submitted = request.args.get('is_submitted', 'false').lower() == 'true'
    user_id = get_jwt_identity()

    if not level_id:
        return jsonify({'message': 'Level ID is required'}), 400

    max_level_id = db.session.query(db.func.max(Level.id)).scalar()
    min_level_id = db.session.query(db.func.min(Level.id)).scalar()

    if level_id < min_level_id or level_id > max_level_id:
        return jsonify({'message': 'Invalid level ID'}), 400

    level_name = Level.query.get(level_id).name

    level_list = [level_id]
    level_answers = get_user_answers(user_id, level_list, False) or get_user_answers(user_id, level_list, True)
    
    response = {
        'level_id': level_id,
        'level_name': level_name,
        'next_level_id': level_id + 1 if level_id < max_level_id else None,
        'prev_level_id': level_id - 1 if level_id > min_level_id else None,
        'answers': []
    }

    for user_answer in level_answers:
        answer = Answer.query.get(user_answer.answer_id)
        question = Question.query.get(answer.question_id)
        response['answers'].append({
            'question_id': question.id,
            'max_points': 5,
            'user_points': answer.points
        })

    return jsonify(response), 200


@answers_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit():
    data = request.get_json()
    level_id = data.get('level_id')
    user_id = get_jwt_identity()

    if not level_id:
        return jsonify({'message': 'Level ID is required'}), 400
    
    # get all answer ids for this level
    answer_ids = db.session.query(Answer.id) \
        .join(Question, Answer.question_id == Question.id) \
        .filter(Question.level_id == level_id) \
        .all()
    answer_ids = [answer_id[0] for answer_id in answer_ids]

    # update all user answers for this level to submitted
    UserAnswer.query \
        .filter_by(user_id=user_id, is_submitted=False) \
        .filter(UserAnswer.answer_id.in_(answer_ids)) \
        .update({UserAnswer.is_submitted: True}, synchronize_session=False)

    db.session.commit()
    return jsonify({'message': 'Answers submitted successfully'}), 200
