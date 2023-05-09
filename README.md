# django-friends-service

This is REST API for implementing a friend system in your application. The API provides functionality for sending friend requests, approving or declining incoming friend requests, and managing friendships.

## Getting Started

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/Dana299/django-friends-service.git
```

You can install all the required packages using `pip`:

```bash
pip install -r requirements.txt
```

### Running the Application

After installing the required packages, navigate to the project directory and run the following commands to set up the database and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

The following endpoints are available in the API:

- `/register/`: Register a new user.
- `/login/`: Login a user.
- `/logout/`: Logout a user.
- `/requests/`: Get list of incoming or outcoming friend requests.
- `/requests/<str:username>/`: Approve or decline a friend request from the given user.
- `/friends/`: Get the list of friends of the current user.
- `/friends/<str:username>/`: Delete a friend with the given username.
- `/friends/status/<str:username>/`: Get the relationship status between the current user and the user with the given username.

## API Documentation

Detailed API documentation was genereated with Swagger. It is available at `http://127.0.0.1:8000/docs/`.
