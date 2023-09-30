import dateutil.parser
import babel
from flask import Flask, request, jsonify, abort, render_template
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from auth import AuthError, requires_auth
import markdown
from models import setup_db, Movie, Actor, db

def create_app(test_config=None):
    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # Filters
    def format_datetime(value, format='medium'):
        date = dateutil.parser.parse(value)
        if format == 'full':
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format, locale='en')

    app.jinja_env.filters['datetime'] = format_datetime
    
##########################################################################
##########################################################################
# Movies
##########################################################################
##########################################################################
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = [movie.format() for movie in movies]

            return jsonify({
                "success": True,
                "movies": formatted_movies,
                "total_movies": len(movies)
            })
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie_by_id(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                return jsonify({
                    'success': False,
                    'error': 404,
                    'message': f'Movie with ID {movie_id} not found.'
                }), 404

            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movies')
    def create_movie(payload):
        try:
            data = request.get_json()
            new_movie = Movie(**data)
            new_movie.insert()

            return jsonify({
                "success": True,
                "movie": new_movie.format()
            }), 201  # 201 Created status code
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                return jsonify({
                    'success': False,
                    'error': 404,
                    'message': f'Movie with ID {movie_id} not found.'
                }), 404

            movie.delete()

            return jsonify({
                'success': True,
                'deleted_movie_id': movie_id
            })
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')  
    def update_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                return jsonify({
                    'success': False,
                    'error': 404,
                    'message': f'Movie with ID {movie_id} not found.'
                }), 404

            data = request.get_json()

            for key, value in data.items():
                setattr(movie, key, value)

            movie.update()

            return jsonify({
                'success': True,
                'updated_movie': movie.format()
            })
        except Exception as e:
            print(e)
            abort(500)

##########################################################################
##########################################################################
# Actors
##########################################################################
##########################################################################
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in actors]

            return jsonify({
                "success": True,
                "actors": formatted_actors,
                "total_actors": len(actors)
            })
        except Exception as e:
            print(e)
            abort(500) 

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor_by_id(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if actor is None:
                return jsonify({
                    'success': False,
                    'error': 404,
                    'message': f'Actor with ID {actor_id} not found.'
                }), 404

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actors')
    def create_actor(payload):
        try:
            data = request.get_json()
            new_actor = Actor(**data)
            new_actor.insert()

            return jsonify({
                "success": True,
                "actor": new_actor.format()
            }), 201  # 201 Created status code
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if actor is None:
                return jsonify({
                    'success': False,
                    'error': 404,
                    'message': f'Actor with ID {actor_id} not found.'
                }), 404

            actor.delete()

            return jsonify({
                'success': True,
                'deleted_actor_id': actor_id
            })
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')  
    def update_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if actor is None:
                return jsonify({
                    'success': False,
                    'error': 404,
                    'message': f'Actor with ID {actor_id} not found.'
                }), 404

            data = request.get_json()

            for key, value in data.items():
                setattr(actor, key, value)

            actor.update()

            return jsonify({
                'success': True,
                'updated_actor': actor.format()
            })
        except Exception as e:
            print(e)
            abort(500)



    return app


app = create_app() 

if __name__ == '__main__':
    app.run()