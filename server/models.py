from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db, metadata


# Association table
episode_guests = db.Table(
    'episodes_guests',
    metadata,
    db.Column('episode_id', db.Integer, db.ForeignKey('episode.id'), primary_key=True),
    db.Column('guest_id', db.Integer, db.ForeignKey('guest.id'), primary_key=True)
)
class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    # Relationship mapping episode to guests
    guests = db.relationship('Guest', secondary='episode_guests', back_populates='episodes')

    # Relationship mapping episode to appearances
    appearances = db.relationship('Appearance', back_populates='episode', cascades='all, delete-orphan')

    # Association proxy to access guest directly
    guests_direct = association_proxy('appearances', 'guest', creator=lambda guest_obj: Appearance(guest=guest_obj))

    def __repr__(self):
        return f'<ID: {self.id},  Date: {self.date}, Number: {self.number}>'
    
class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    # Relationship mapping guest to episodes
    episodes = db.relationship('Episode', secondary='episode_guests', back_populates='guests')

    # Relationship mapping guest to appearances
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    # Association proxy to access episode directly
    episodes_direct = association_proxy('appearances', 'episode', creator=lambda episode_obj: Appearance(episode=episode_obj))

    def __repr__(self):
        return f'ID: {self.id}, Name: {self.name}, Occupation: {self.occupation}'
    
class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    # Foreign Keys
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))

    # Relationship mapping appearance to episode
    episode = db.relationship('Episode', back_populates='appearances')

    # Relationship mapping appearance to guest
    guest = db.relationship('Guest', back_populates='appearances')

    @validates('rating')
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:
            raise ValueError('Rating must be between 1 and 5')

    def __repr__(self):
        return f'ID: {self.id}, Rating: {self.rating}'