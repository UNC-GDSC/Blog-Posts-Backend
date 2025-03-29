# Blog API with Flask & SQLAlchemy

This project is a simple backend API for managing blog posts built using Python's Flask framework and SQLAlchemy. It provides CRUD (Create, Read, Update, Delete) operations for blog posts and can serve as a starting point for more advanced blog or content management systems.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Tech Stack](#tech-stack)
5. [Installation & Setup](#installation--setup)
6. [Usage](#usage)
    - [API Endpoints](#api-endpoints)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Future Enhancements](#future-enhancements)
10. [Troubleshooting & FAQ](#troubleshooting--faq)
11. [Contributing](#contributing)
12. [License](#license)

---

## Overview

The Blog API is a RESTful service that allows clients to manage blog posts. It supports the following operations:
- Retrieve all blog posts
- Retrieve a single post by ID
- Create a new post
- Update an existing post
- Delete a post

The API is built using Flask for the web framework and SQLAlchemy for ORM (Object Relational Mapping) with a SQLite database for data persistence.

---

## Features

- **CRUD Operations:** Full support for creating, reading, updating, and deleting blog posts.
- **RESTful Design:** Standardized endpoints and HTTP methods for API operations.
- **Lightweight & Simple:** Minimal dependencies, making it easy to set up and extend.
- **Data Serialization:** Returns JSON responses for easy consumption by clients (web or mobile).
- **Auto-updating Timestamps:** Automatically records when posts are created and updated.

---

## Architecture

### System Overview

- **Flask App:** Handles incoming HTTP requests and routes them to appropriate handlers.
- **SQLAlchemy ORM:** Maps Python objects to database records, simplifying database interactions.
- **SQLite Database:** Stores blog posts; ideal for development and testing.

### Component Breakdown

1. **API Endpoints:**  
   The application defines endpoints for:
   - Listing all posts
   - Getting a single post
   - Creating a new post
   - Updating a post
   - Deleting a post

2. **Model Definition:**  
   The `Post` model defines the structure of a blog post, including fields for title, content, and timestamps for creation and updates.

3. **Data Serialization:**  
   Each post is converted to a dictionary format via the `to_dict()` method before being sent as JSON in the response.

---

## Tech Stack

- **Programming Language:** Python 3.x
- **Web Framework:** Flask
- **ORM:** SQLAlchemy
- **Database:** SQLite (for simplicity; can be switched to PostgreSQL/MySQL for production)
- **Dependency Management:** pip

---

## Installation & Setup

### Prerequisites

- Python 3.x installed on your system.
- `pip` for installing Python packages.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/blog-api.git
   cd blog-api
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install flask flask_sqlalchemy
   ```

4. **Run the Application**

   The application will automatically create the SQLite database and required tables on the first run.

   ```bash
   python app.py
   ```

   The API will now be accessible at [http://localhost:5000](http://localhost:5000).

---

## Usage

### API Endpoints

#### 1. Get All Posts

- **Endpoint:** `GET /posts`
- **Description:** Retrieve a list of all blog posts.
- **Response:**

  ```json
  [
    {
      "id": 1,
      "title": "My First Post",
      "content": "This is the content of my first post.",
      "created_at": "2025-03-29T12:34:56.789123",
      "updated_at": "2025-03-29T12:34:56.789123"
    },
    ...
  ]
  ```

#### 2. Get a Single Post

- **Endpoint:** `GET /posts/<post_id>`
- **Description:** Retrieve details of a specific post by its ID.
- **Example:** `GET /posts/1`
- **Response:**

  ```json
  {
    "id": 1,
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "created_at": "2025-03-29T12:34:56.789123",
    "updated_at": "2025-03-29T12:34:56.789123"
  }
  ```

#### 3. Create a New Post

- **Endpoint:** `POST /posts`
- **Description:** Create a new blog post.
- **Request Body:**

  ```json
  {
    "title": "My New Post",
    "content": "Content for my new post."
  }
  ```

- **Response:**  
  Returns the created post with a unique ID and timestamps.

  ```json
  {
    "id": 2,
    "title": "My New Post",
    "content": "Content for my new post.",
    "created_at": "2025-03-29T13:00:00.000000",
    "updated_at": "2025-03-29T13:00:00.000000"
  }
  ```

#### 4. Update an Existing Post

- **Endpoint:** `PUT /posts/<post_id>`
- **Description:** Update the title and/or content of an existing post.
- **Request Body:**

  ```json
  {
    "title": "Updated Title",
    "content": "Updated content."
  }
  ```

- **Response:**  
  Returns the updated post.

  ```json
  {
    "id": 1,
    "title": "Updated Title",
    "content": "Updated content.",
    "created_at": "2025-03-29T12:34:56.789123",
    "updated_at": "2025-03-29T14:00:00.000000"
  }
  ```

#### 5. Delete a Post

- **Endpoint:** `DELETE /posts/<post_id>`
- **Description:** Delete a post by its ID.
- **Response:**

  ```json
  {
    "message": "Post deleted successfully."
  }
  ```

---

## Testing

### Unit Testing

- You can write tests using Python's `unittest` or `pytest` modules.
- Test the functionality of each endpoint (e.g., ensure a new post is created, retrieval returns correct data, updates persist, etc.).

### Example with `pytest`

1. **Install pytest:**

   ```bash
   pip install pytest
   ```

2. **Create a test file (e.g., `test_app.py`) and write tests:**

   ```python
   import json
   from app import app, db, Post

   def test_get_posts():
       with app.test_client() as client:
           response = client.get('/posts')
           assert response.status_code == 200

   def test_create_post():
       with app.test_client() as client:
           data = {
               "title": "Test Post",
               "content": "This is a test."
           }
           response = client.post('/posts', json=data)
           assert response.status_code == 201
           json_data = json.loads(response.data)
           assert json_data['title'] == "Test Post"
   ```

3. **Run the tests:**

   ```bash
   pytest
   ```

---

## Deployment

### Docker

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run the Docker container:

```bash
docker build -t blog-api .
docker run -d -p 5000:5000 blog-api
```

### Cloud Deployment

- Use platforms like Heroku, AWS Elastic Beanstalk, or Google Cloud Run.
- Ensure environment variables and database settings are configured for production.
- Configure logging and monitoring.

---

## Future Enhancements

- **User Authentication:** Secure endpoints so only authorized users can create or modify posts.
- **Pagination:** Add pagination for the `GET /posts` endpoint.
- **Search Functionality:** Implement search capabilities for blog posts.
- **Frontend Interface:** Develop a frontend dashboard using React or Vue.js.
- **Advanced Error Handling:** Improve error messages and logging for better debugging.

---

## Troubleshooting & FAQ

- **Application Not Starting:**  
  Ensure that all dependencies are installed and the virtual environment is activated.
  
- **Database Issues:**  
  Verify that the SQLite file is accessible or update the `SQLALCHEMY_DATABASE_URI` for other database systems.

- **API Returns 404:**  
  Make sure you are using the correct URL and that the server is running on the expected port.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes.
4. Push the branch (`git push origin feature/my-feature`).
5. Open a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy using the Blog API, and feel free to extend it further to suit your needs!
