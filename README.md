# Face Recognition Backend

This project is a backend service for a face recognition system. It provides APIs for user authentication (signup, login) and face verification.

## Features

- **User Signup:** Register new users with their name, email, contact, password, and a clear face image.
- **User Login:** Authenticate users with their email and password.
- **Face Verification:** Verify a user's identity by comparing their face with the registered face.
- **Face Comparison:** Compare two faces to check if they belong to the same person.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/face-recognition-backend.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd face-recognition-backend
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

The application will be running at `http://127.0.0.1:8000`.

## API Endpoints

The following are the available API endpoints:

- `POST /auth/signup`: Register a new user.
- `POST /auth/login`: Login an existing user.
- `POST /auth/verify-face`: Verify a user's face for authentication.
- `POST /auth/compare-face`: Compare two faces to check for similarity.

### `POST /auth/signup`

Registers a new user.

**Request Body:**

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "contact": "1234567890",
  "password": "your-password",
  "image": "data:image/jpeg;base64,..."
}
```

### `POST /auth/login`

Logs in an existing user.

**Request Body:**

```json
{
  "email": "john.doe@example.com",
  "password": "your-password"
}
```

### `POST /auth/verify-face`

Verifies a user's face.

**Request Body:**

```json
{
  "email": "john.doe@example.com",
  "image": "data:image/jpeg;base64,..."
}
```

### `POST /auth/compare-face`

Compares two faces.

**Request Body:**

```json
{
  "image1": "data:image/jpeg;base64,...",
  "image2": "data:image/jpeg;base64,..."
}
```

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- [FaceNet](https://github.com/davidsandberg/facenet): A unified embedding for face recognition and clustering.
- [MediaPipe](https://google.github.io/mediapipe/): A cross-platform, customizable ML solutions for live and streaming media.
- [SQLAlchemy](https://www.sqlalchemy.org/): The Python SQL Toolkit and Object Relational Mapper.
- [Uvicorn](https://www.uvicorn.org/): An ASGI server implementation, for use with FastAPI.