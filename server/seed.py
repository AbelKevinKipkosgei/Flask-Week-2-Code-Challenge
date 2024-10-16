import json
import random
from config import db, app
from models import Episode, Guest, Appearance, episode_guests

with app.app_context():

    # Delete all rows in tables
    db.session.query(episode_guests).delete()
    db.session.query(Episode).delete()
    db.session.query(Guest).delete()
    db.session.query(Appearance).delete()
    db.session.commit()

    # Load data from seed.json
    try:
        with open('seed.json', 'r') as f:
            data = json.load(f)  
    except FileNotFoundError:
        print("seed.json not found")
        exit()
    except json.JSONDecodeError:
        print("Invalid JSON in seed.json")
        exit()
    episode_counter = 0

    for entry in data:
        # Extracting relevant fields from each entry
        year = entry['YEAR']
        occupation = entry['GoogleKnowlege_Occupation']
        show_date = entry['Show']
        raw_guest_list = entry['Raw_Guest_List']

        # Create a new Guest object
        guest = Guest(name=raw_guest_list, occupation=occupation)

        # Create a new Episode object
        episode = Episode(date=show_date, number=episode_counter)

        # Random rating
        random_rating = random.randint(1, 5)

        # Create an Appearance object that associates the Guest with the Episode
        appearance = Appearance(rating=random_rating, guest=guest, episode=episode)

        # Add the objects to the session
        db.session.add(guest)
        db.session.add(episode)
        db.session.add(appearance)

        # Increment episode counter for the next event
        episode_counter += 1

    # Commit the session to save the changes
    db.session.commit()
    print("Data seeded successfully!")
