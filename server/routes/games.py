from flask import jsonify, Response, Blueprint, request
from models import db, Game, Publisher, Category
from sqlalchemy.orm import Query

# Create a Blueprint for games routes
games_bp = Blueprint('games', __name__)

def get_games_base_query() -> Query:
    """
    Build the base query for games with joined publisher and category data.
    
    Returns:
        Query: SQLAlchemy query object with games joined to publishers and categories
    """
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
    """
    Retrieve all games with their associated publisher and category information.
    
    Returns:
        Response: JSON response containing an array of game objects with publisher and category details
    """
    # Use the base query for all games
    games_query = get_games_base_query().all()
    
    # Convert the results using the model's to_dict method
    games_list = [game.to_dict() for game in games_query]
    
    return jsonify(games_list)

@games_bp.route('/api/games/<int:id>', methods=['GET'])
def get_game(id: int) -> tuple[Response, int] | Response:
    """
    Retrieve a specific game by its ID with associated publisher and category information.
    
    Args:
        id: The unique identifier of the game to retrieve
        
    Returns:
        Response: JSON response containing the game object with publisher and category details,
                 or error response with 404 status if game not found
    """
    # Use the base query and add filter for specific game
    game_query = get_games_base_query().filter(Game.id == id).first()
    
    # Return 404 if game not found
    if not game_query: 
        return jsonify({"error": "Game not found"}), 404
    
    # Convert the result using the model's to_dict method
    game = game_query.to_dict()
    
    return jsonify(game)

@games_bp.route('/api/games', methods=['POST'])
def create_game() -> tuple[Response, int]:
    # Check content type first
    if not request.is_json:
        return jsonify({"error": "Request body must be valid JSON"}), 400
    
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400
    
    required_fields = ['title', 'description', 'category_id', 'publisher_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        # Validate that category and publisher exist
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({"error": "Category not found"}), 400
            
        publisher = Publisher.query.get(data['publisher_id'])
        if not publisher:
            return jsonify({"error": "Publisher not found"}), 400
        
        # Create new game - validation happens in the model
        game = Game(
            title=data['title'],
            description=data['description'],
            category_id=data['category_id'],
            publisher_id=data['publisher_id'],
            star_rating=data.get('star_rating')  # Optional field
        )
        
        # Add to database
        db.session.add(game)
        db.session.commit()
        
        # Return the created game
        return jsonify(game.to_dict()), 201
        
    except ValueError as e:
        # Handle model validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle any other database errors
        db.session.rollback()
        return jsonify({"error": "Failed to create game"}), 500

@games_bp.route('/api/games/<int:id>', methods=['PUT'])
def update_game(id: int) -> tuple[Response, int] | Response:
    # Get the game to update
    game = Game.query.get(id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    # Check content type first
    if not request.is_json:
        return jsonify({"error": "Request body must be valid JSON"}), 400
    
    # Get JSON data from request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400
    
    try:
        # Update fields if provided
        if 'title' in data:
            game.title = data['title']
        if 'description' in data:
            game.description = data['description']
        if 'star_rating' in data:
            game.star_rating = data['star_rating']
        
        # Handle category_id update
        if 'category_id' in data:
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({"error": "Category not found"}), 400
            game.category_id = data['category_id']
        
        # Handle publisher_id update  
        if 'publisher_id' in data:
            publisher = Publisher.query.get(data['publisher_id'])
            if not publisher:
                return jsonify({"error": "Publisher not found"}), 400
            game.publisher_id = data['publisher_id']
        
        # Commit changes
        db.session.commit()
        
        # Return updated game
        return jsonify(game.to_dict())
        
    except ValueError as e:
        # Handle model validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle any other database errors
        db.session.rollback()
        return jsonify({"error": "Failed to update game"}), 500

@games_bp.route('/api/games/<int:id>', methods=['DELETE'])
def delete_game(id: int) -> tuple[Response, int]:
    # Get the game to delete
    game = Game.query.get(id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    try:
        # Delete the game
        db.session.delete(game)
        db.session.commit()
        
        # Return success message
        return jsonify({"message": "Game deleted successfully"}), 200
        
    except Exception as e:
        # Handle any database errors
        db.session.rollback()
        return jsonify({"error": "Failed to delete game"}), 500
