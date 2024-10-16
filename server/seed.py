# seed.py

from faker import Faker
from models import db, Episode, Guest, Appearance  # Adjust import based on your structure

fake = Faker()

def create_fake_guests(num_guests=10):
    guests = []
    for _ in range(num_guests):
        guest = Guest(
            name=fake.name(),
            occupation=fake.job()
        )
        guests.append(guest)
    return guests

def create_fake_episodes(num_episodes=10):
    episodes = []
    for _ in range(num_episodes):
        episode = Episode(
            date=fake.date(),
            number=fake.random_int(min=1, max=100)
        )
        episodes.append(episode)
    return episodes

def create_fake_appearances(episodes, guests):
    appearances = []
    for episode in episodes:
        # Randomly select a guest for this episode
        guest = fake.random_element(elements=guests)
        # Create a random rating
        rating = fake.random_int(min=1, max=5)
        
        appearance = Appearance(
            rating=rating,
            episode=episode,
            guest=guest
        )
        appearances.append(appearance)
    return appearances

def seed_database():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create fake data
    guests = create_fake_guests(num_guests=10)
    episodes = create_fake_episodes(num_episodes=10)
    
    # Add guests and episodes to the session
    db.session.add_all(guests)
    db.session.add_all(episodes)
    db.session.commit()  # Commit to generate IDs before creating appearances

    # Create appearances
    appearances = create_fake_appearances(episodes, guests)
    
    # Add appearances to the session
    db.session.add_all(appearances)
    
    # Commit the session to save data
    db.session.commit()
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    from app import app  # Adjust import based on your structure
    with app.app_context():
        seed_database()
