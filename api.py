from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, current_user
from models import db, Post, User

api = Blueprint('api', __name__)

# Helper function to validate input data
def validate_post_data(data):
    if not data or 'title' not in data or 'content' not in data:
        return {"error": "Invalid input, 'title' and 'content' are required"}, 400
    return None

@api.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])

@api.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    
    # Validate input data
    error = validate_post_data(data)
    if error:
        return jsonify(error), 400
    
    # Create a new post
    post = Post(title=data['title'], content=data['content'], author=current_user)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@api.route('/api/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_dict())

@api.route('/api/posts/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    post = Post.query.get_or_404(id)
    
    # Ensure that the current user is the author of the post
    if post.author != current_user:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    
    # Validate input data
    error = validate_post_data(data)
    if error:
        return jsonify(error), 400
    
    # Update the post
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify(post.to_dict())

@api.route('/api/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get_or_404(id)
    
    # Ensure that the current user is the author of the post
    if post.author != current_user:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Delete the post
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"})
