# server/app.py
#!/usr/bin/env python3

from sqlite3 import IntegrityError
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

class EpisodesResource(Resource):
    def get(self):
        episodes = [episode.to_dict() for episode in Episode.query.all()]
        return make_response(jsonify(episodes), 200)
    
class EpisodesResourceById(Resource):
    def get(self, id):
        episode = Episode.query.filter_by(id = id).first()
        if not episode:
            return make_response(jsonify({
                'error': 'Episode not found'
            }))
        return make_response(jsonify(episode.to_dict()), 200)
    
    def delete(self, id):
        # Get the episode from the database
        episode = Episode.query.filter(Episode.id == id).first()
        db.session.delete(episode)
        db.session.commit()

        return  make_response(jsonify({
            'message': 'Episode deleted'
        }))
    
class GuestsResource(Resource):
    def get(self):
        guests = [guest.to_dict() for guest in Guest.query.all()]
        return make_response(jsonify(guests), 200)
    
class AppearanceResource(Resource):
    def post(self):
        data = request.get_json()

        # Validate incoming data
        if not data or 'rating' not in data or 'episode_id' not in data or 'guest_id' not in data:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)
        
         # Create a new Appearance
        appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )

        try:
            db.session.add(appearance)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({"errors": ["validation errors"]}), 400)
        
        # Response data
        appearance_data = {
            'id': appearance.id,
            'rating': appearance.rating,
            'episode_id': appearance.episode_id,
            'guest_id': appearance.guest_id
        }

        episode = Episode.query.filter(Episode.id == data['episode_id']).first()
        episode_data = {
            'date':  episode.date,
            'id': episode.id,
            'number': episode.number
        }

        guest = Guest.query.filter(Guest.id == data['guest_id']).first()
        guest_data = {
            'id': guest.id,
            'name': guest.name,
            'occupation': guest.occupation
        }


        response_data = {
            **appearance_data,
            'episode': episode_data,
            'guest': guest_data
        }

        return make_response(jsonify(response_data), 201)
    

api.add_resource(EpisodesResource, '/episodes')
api.add_resource(EpisodesResourceById, '/episodes/<int:id>')
api.add_resource(GuestsResource, '/guests')
api.add_resource(AppearanceResource, '/appearances')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
