# Social Media API - Backend Capstone Project

This repository contains the backend implementation for a Social Media API built using **Django** and **Django REST Framework**. The API provides core functionality such as posts, user authentication, and follows. It uses MySQL as the database.

## Table of Contents

1. [Project Overview](#project-overview)
2. [API Endpoints](#api-endpoints)
    - [Fetch All Posts](#fetch-all-posts)
    - [Create a Post](#create-a-post)
3. [Authentication](#authentication)
4. [Testing Endpoints](#testing-endpoints)
    - [Postman](#testing-with-postman)
    - [cURL](#testing-with-curl)
5. [Setup Instructions](#setup-instructions)
6. [Contributing](#contributing)

## Project Overview

The Social Media API provides endpoints for managing posts and users, implementing basic authentication using Django's built-in authentication system. It allows users to:
- Fetch, create, update, and delete posts.
- Register, log in, and manage user accounts.

The project also demonstrates basic **Django ORM** usage for interacting with the database and includes test coverage for core functionality.

---

## API Endpoints

### Fetch All Posts
- **Path**: `/api/posts/`
- **Method**: `GET`
- **Description**: Fetch all the posts available in the database.
- **Request Parameters**: None
- **Response**: A list of posts in JSON format.

#### Example Response:

```json
[
  {
    "id": 1,
    "title": "My First Post",
    "content": "This is the content of my first post",
    "user": 1,
    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-01T12:00:00Z"
  },
  {
    "id": 2,
    "title": "Another Post",
    "content": "This is another post",
    "user": 2,
    "created_at": "2025-01-02T12:00:00Z",
    "updated_at": "2025-01-02T12:00:00Z"
  }
]

Create a Post
Path: /api/posts/
Method: POST
Description: Create a new post.
Request Parameters:
title: (string) The title of the post.
content: (string) The content of the post.
user: (integer) The ID of the user creating the post.
Response: The created post in JSON format.
Example Request:
json
Copy code
{
  "title": "New Post",
  "content": "This is the content of the new post",
  "user": 1
}
Example Response:
json
Copy code
{
  "id": 3,
  "title": "New Post",
  "content": "This is the content of the new post",
  "user": 1,
  "created_at": "2025-01-12T12:00:00Z",
  "updated_at": "2025-01-12T12:00:00Z"
}
Authentication
This API uses Django's built-in authentication system for securing endpoints. The following authentication methods are supported:

Session Authentication (default): Users must log in to create or view posts.
Setup
To enable authentication:

Install dependencies:

bash
Copy code
pip install -r requirements.txt
Migrate the database:

bash
Copy code
python manage.py migrate
Create a superuser to manage users:

bash
Copy code
python manage.py createsuperuser
Login to access protected endpoints.

Testing Endpoints
Testing with Postman
GET /api/posts/:

Set method to GET.
URL: http://localhost:8000/api/posts/
Hit Send to retrieve a list of posts.
POST /api/posts/:

Set method to POST.
URL: http://localhost:8000/api/posts/
In the Body tab, set raw and choose JSON. Add the post’s data like:
json
Copy code
{
  "title": "New Post",
  "content": "This is the content of the new post",
  "user": 1
}
Hit Send to create a new post.
Testing with cURL
GET /api/posts/:

bash
Copy code
curl -X GET http://localhost:8000/api/posts/
POST /api/posts/:

bash
Copy code
curl -X POST http://localhost:8000/api/posts/ -H "Content-Type: application/json" -d '{"title": "New Post", "content": "This is the content of the new post", "user": 1}'
Setup Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/social-media-api.git
cd social-media-api
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Apply database migrations:

bash
Copy code
python manage.py migrate
Create a superuser (if needed):

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
