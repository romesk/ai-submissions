from flask import Blueprint

from .auth import auth_bp
from .questions import questions_bp
from .answers import answers_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(questions_bp)
api_bp.register_blueprint(answers_bp)



