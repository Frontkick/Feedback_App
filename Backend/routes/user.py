from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import User, Feedback
from schemas import UserSchema, FeedbackSchema

user_bp = Blueprint('user', __name__)

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def profile():
    identity = get_jwt_identity()  # user ID as string
    user = User.query.get(int(identity))
    return jsonify(UserSchema().dump(user))

@user_bp.route('/feedback', methods=['GET'])
@jwt_required()
def my_feedback():
    identity = get_jwt_identity()
    claims = get_jwt()
    if claims['role'] != 'employee':
        return jsonify({'msg': 'Forbidden'}), 403
    feedbacks = Feedback.query.filter_by(employee_id=int(identity)).all()
    return jsonify(FeedbackSchema(many=True).dump(feedbacks))
