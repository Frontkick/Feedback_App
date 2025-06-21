from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from database import db
from models import User, Feedback
from schemas import FeedbackSchema, UserSchema
import yagmail

# Blueprints
feedback_bp = Blueprint('feedback', __name__)

# Constants for email
SENDER_EMAIL = "hellfire7746@gmail.com"
APP_PASSWORD = "ptmghofjmlxfpnub"  # Use actual app password

@feedback_bp.route('/', methods=['POST'])
@jwt_required()
def create_feedback():
    identity = get_jwt_identity()
    claims = get_jwt()
    if claims['role'] != 'manager':
        return jsonify({'msg': 'Forbidden'}), 403

    data = request.get_json()
    fb = Feedback(**data, manager_id=int(identity))
    db.session.add(fb)
    db.session.commit()

    employee = User.query.get(fb.employee_id)
    if employee and employee.email:
        yag = yagmail.SMTP(user=SENDER_EMAIL, password=APP_PASSWORD)
        subject_text = "✅ You have new feedback"
        html_content = f"""
        <h2 style="color:#4CAF50;">New Feedback Received</h2>
        <p>Hi {employee.username},</p>
        <p>Your manager has just given you new feedback.</p>
        <a href="https://feedback-frontend-sigma.vercel.app" style="padding:10px 15px; background-color:#4CAF50; color:white; text-decoration:none; border-radius:5px;">View Feedback</a>
        """
        yag.send(employee.email, subject_text, html_content)

    return jsonify(FeedbackSchema().dump(fb)), 201

@feedback_bp.route('/<int:fid>', methods=['PUT'])
@jwt_required()
def update_feedback(fid):
    identity = get_jwt_identity()
    claims = get_jwt()
    fb = Feedback.query.get_or_404(fid)
    if claims['role'] != 'manager' or fb.manager_id != int(identity):
        return jsonify({'msg': 'Forbidden'}), 403
    data = request.get_json()
    for k, v in data.items():
        setattr(fb, k, v)
    db.session.commit()
    return jsonify(FeedbackSchema().dump(fb)), 200

@feedback_bp.route('/<int:fid>/acknowledge', methods=['PUT'])
@jwt_required()
def acknowledge_feedback(fid):
    identity = get_jwt_identity()
    claims = get_jwt()
    fb = Feedback.query.get_or_404(fid)
    if claims['role'] != 'employee' or fb.employee_id != int(identity):
        return jsonify({'msg': 'Forbidden'}), 403
    fb.acknowledged = True
    db.session.commit()
    return jsonify(FeedbackSchema().dump(fb)), 200

@feedback_bp.route('/<int:fid>/comment', methods=['PUT'])
@jwt_required()
def add_employee_comment(fid):
    identity = get_jwt_identity()
    claims = get_jwt()
    feedback = Feedback.query.get_or_404(fid)
    if claims['role'] != 'employee' or feedback.employee_id != int(identity):
        return jsonify({'msg': 'Forbidden'}), 403
    data = request.get_json()
    comment = data.get('employee_comments')
    if not comment:
        return jsonify({'msg': 'Comment is required'}), 400
    feedback.employee_comments = comment
    db.session.commit()
    return jsonify(FeedbackSchema().dump(feedback)), 200

@feedback_bp.route('/given', methods=['GET'])
@jwt_required()
def feedbacks_given_by_manager():
    identity = get_jwt_identity()
    claims = get_jwt()
    if claims['role'] != 'manager':
        return jsonify({'msg': 'Forbidden'}), 403
    feedbacks = Feedback.query.filter_by(manager_id=int(identity)).all()
    data = []
    for fb in feedbacks:
        employee = User.query.get(fb.employee_id)
        fb_data = FeedbackSchema().dump(fb)
        fb_data['employee_username'] = employee.username if employee else None
        data.append(fb_data)
    return jsonify(data), 200

@feedback_bp.route('/team-overview', methods=['GET'])
@jwt_required()
def team_overview():
    identity = get_jwt_identity()
    claims = get_jwt()
    if claims['role'] != 'manager':
        return jsonify({'msg': 'Forbidden'}), 403
    employee_ids = (
        db.session.query(Feedback.employee_id)
        .filter(Feedback.manager_id == int(identity))
        .distinct()
        .all()
    )
    employee_count = len(employee_ids)
    total_feedbacks = Feedback.query.filter_by(manager_id=int(identity)).count()
    sentiments = (
        db.session.query(Feedback.sentiment, db.func.count(Feedback.id))
        .filter(Feedback.manager_id == int(identity))
        .group_by(Feedback.sentiment)
        .all()
    )
    sentiment_breakdown = {s: 0 for s in ['positive', 'neutral', 'negative']}
    for sentiment, count in sentiments:
        sentiment_breakdown[sentiment] = count
    return jsonify({
        "employees_count": employee_count,
        "total_feedbacks": total_feedbacks,
        "sentiment_breakdown": sentiment_breakdown
    }), 200

@feedback_bp.route('/employees', methods=['GET'])
@jwt_required()
def list_employees():
    claims = get_jwt()
    if claims['role'] != 'manager':
        return jsonify({'msg': 'Forbidden'}), 403
    employees = User.query.filter_by(role='employee').all()
    return jsonify(UserSchema(many=True, only=('id','username')).dump(employees)), 200
