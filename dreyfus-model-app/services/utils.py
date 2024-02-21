
from models import Level, Question, Answer, db


def validate_answers(answers: list[int]) -> bool:
    if not answers:
        return False
    
    max_answer_id = db.session.query(db.func.max(Answer.id)).scalar()
    if max_answer_id < max(answers) or min(answers) < 1:
        return False

    # check if all question ids are different and under the same level
    question_ids = [Answer.query.get(answer_id).question_id for answer_id in answers]
    if len(question_ids) != len(set(question_ids)):
        return False
    
    # check if all answers are under the same level
    level_ids = [Question.query.get(question_id).level_id for question_id in question_ids]
    if len(set(level_ids)) != 1:
        return False
    
    # Check if answer amount is the same as required
    level_question_amount = Question.query.filter_by(level_id=level_ids[0]).count()
    if len(answers) != level_question_amount:
        return False
    
    return True