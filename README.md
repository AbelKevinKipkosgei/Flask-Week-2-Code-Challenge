# Flask Podcast Management App

This Flask application provides a RESTful API for managing podcasts, featuring episodes, guests, and their appearances. It leverages SQLAlchemy for ORM and uses SQLite as the database. The application is structured to allow easy scalability and maintenance.

## Features

- **Episode Management**: Create, retrieve, and delete podcast episodes.
- **Guest Management**: Retrieve a list of guests featured in episodes.
- **Appearance Management**: Record the appearance of guests in episodes with ratings.
- **Data Seeding**: Populate the database with fake data using the Faker library.

## Technologies

- **Flask**: A micro web framework for Python.
- **Flask-Restful**: An extension for Flask that adds support for quickly building REST APIs.
- **SQLAlchemy**: An ORM that provides a full power and flexibility of SQL.
- **SQLite**: A lightweight database for easy data storage.
- **Faker**: A library to generate fake data for testing and development.

## Setup Instructions

1. **Clone the Repository**:
   git clone https://github.com/AbelKevinKipkosgei/python-p4-iam-putting-it-all-together-lab
   Use code . to open in VScode from terminal.
   cd server

2. **Install Dependencies and set Up a Virtual Environment**:
   pipenv install && pipenv shell 


3. **Run Migrations**:
   Migrations have been setup but feel free to migrate any changes using
   the following command:
   flask db migrate -m "your message."
   flask db upgrade head

4. **Run the Application**:
   python server/app.py


## Usage

The application will be running on `http://127.0.0.1:5555`. You can interact with the API using tools like Postman or Insomnia.

## API Endpoints

### Episodes

- **Get All Episodes**
  - **Endpoint**: `GET /episodes`
  - **Response**: Returns a list of all episodes.

- **Get Episode by ID**
  - **Endpoint**: `GET /episodes/<int:id>`
  - **Response**: Returns the episode with the specified ID. If not found, returns a 404 error.

- **Delete Episode by ID**
  - **Endpoint**: `DELETE /episodes/<int:id>`
  - **Response**: Deletes the episode with the specified ID and returns a success message.

### Guests

- **Get All Guests**
  - **Endpoint**: `GET /guests`
  - **Response**: Returns a list of all guests.

### Appearances

- **Create Appearance**
  - **Endpoint**: `POST /appearances`
  - **Request Body**: 
    {
      "rating": <int>,
      "episode_id": <int>,
      "guest_id": <int>
    }
  - **Response**: Returns the created appearance data. If validation fails, returns a 400 error with validation errors.

## Models

### Episode

- **Attributes**:
  - `id`: Primary key.
  - `date`: Date of the episode.
  - `number`: Episode number.
  
- **Relationships**:
  - Many-to-many relationship with `Guest` through `appearance`.
  - One-to-many relationship with `Appearance`.

### Guest

- **Attributes**:
  - `id`: Primary key.
  - `name`: Name of the guest.
  - `occupation`: Occupation of the guest.
  
- **Relationships**:
  - Many-to-many relationship with `Episode` through `appearance`.
  - One-to-many relationship with `Appearance`.

### Appearance

- **Attributes**:
  - `id`: Primary key.
  - `rating`: Rating given for the guest's appearance (1 to 5).
  - `episode_id`: Foreign key to `Episode`.
  - `guest_id`: Foreign key to `Guest`.
  
- **Relationships**:
  - Many-to-one relationship with `Episode`.
  - Many-to-one relationship with `Guest`.

## Seeding the Database

To seed the database with fake data, run the `seed.py` script. This will create a number of guests, episodes, and their appearances.

1. Ensure the application is running.
2. Execute the following command in your terminal:

   python seed.py


After running the seeding script, you should see a message indicating that the database has been seeded successfully.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

Feel free to modify the README according to your specific needs or additional features!

This README provides a comprehensive guide for users and developers to understand and use your Flask application effectively.