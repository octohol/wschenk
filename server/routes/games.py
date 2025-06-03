from flask import jsonify, Response, Blueprint, request
from models import db, Game, Publisher, Category
from sqlalchemy.orm import Query

# Create a Blueprint for games routes
games_bp = Blueprint('games', __name__)

def get_games_base_query() -> Query:
    return db.session.query(Game).join(
        Publisher, 
        Game.publisher_id == Publisher.id, 
        isouter=True
    ).join(
        Category, 
        Game.category_id == Category.id, 
        isouter=True
    )

@games_bp.route('/api/games', methods=['GET'])
def get_games() -> Response:
    # Get filter parameters from query string
    category_filter = request.args.get('category')
    publisher_filter = request.args.get('publisher')
    
    # Start with the base query
    games_query = get_games_base_query()
    
    # Apply category filter if provided
    if category_filter:
        category_ids = [int(id.strip()) for id in category_filter.split(',') if id.strip().isdigit()]
        if category_ids:
            games_query = games_query.filter(Game.category_id.in_(category_ids))
    
    # Apply publisher filter if provided  
    if publisher_filter:
        publisher_ids = [int(id.strip()) for id in publisher_filter.split(',') if id.strip().isdigit()]
        if publisher_ids:
            games_query = games_query.filter(Game.publisher_id.in_(publisher_ids))
    
    # Execute query
    games_list = games_query.all()
    
    # Convert the results using the model's to_dict method
    games_data = [game.to_dict() for game in games_list]
    
    return jsonify(games_data)

@games_bp.route('/api/games/<int:id>', methods=['GET'])
def get_game(id: int) -> tuple[Response, int] | Response:
    # Use the base query and add filter for specific game
    game_query = get_games_base_query().filter(Game.id == id).first()
    
    # Return 404 if game not found
    if not game_query: 
        return jsonify({"error": "Game not found"}), 404
    
    # Convert the result using the model's to_dict method
    game = game_query.to_dict()
    
    return jsonify(game)

@games_bp.route('/api/categories', methods=['GET'])
def get_categories() -> Response:
    # Get all categories
    categories = Category.query.all()
    
    # Convert to dict format
    categories_data = [category.to_dict() for category in categories]
    
    return jsonify(categories_data)

@games_bp.route('/api/publishers', methods=['GET'])  
def get_publishers() -> Response:
    # Get all publishers
    publishers = Publisher.query.all()
    
    # Convert to dict format  
    publishers_data = [publisher.to_dict() for publisher in publishers]
    
    return jsonify(publishers_data)
