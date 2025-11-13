# API Client Examples

This directory contains example code for interacting with the Blog Posts API in different programming languages.

## Available Examples

### 1. Python Client (`python_client.py`)

A complete Python client with methods for all API endpoints.

**Requirements:**
```bash
pip install requests
```

**Usage:**
```python
from python_client import BlogAPIClient

client = BlogAPIClient("http://localhost:5000")

# Create a post
post = client.create_post("My Title", "My content")

# Get all posts
posts = client.get_posts(page=1, per_page=10)

# Search posts
results = client.search_posts("keyword")
```

### 2. JavaScript/Node.js Client (`javascript_client.js`)

A JavaScript/Node.js client using axios.

**Requirements:**
```bash
npm install axios
```

**Usage:**
```javascript
const BlogAPIClient = require('./javascript_client');

const client = new BlogAPIClient('http://localhost:5000');

// Create a post
const post = await client.createPost('My Title', 'My content');

// Get all posts
const posts = await client.getPosts({ page: 1, per_page: 10 });

// Search posts
const results = await client.searchPosts('keyword');
```

### 3. cURL Examples (`curl_examples.sh`)

Shell script with various cURL commands for testing the API.

**Requirements:**
- `curl` command-line tool
- `jq` for JSON formatting (optional)

**Usage:**
```bash
chmod +x curl_examples.sh
./curl_examples.sh
```

Or run individual commands:
```bash
# Health check
curl http://localhost:5000/health

# Get all posts
curl http://localhost:5000/api/v1/posts

# Create a post
curl -X POST http://localhost:5000/api/v1/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "content": "Content here"}'
```

## Common Use Cases

### Creating a Post
```bash
# cURL
curl -X POST http://localhost:5000/api/v1/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "content": "World"}'

# Python
client.create_post("Hello", "World")

# JavaScript
await client.createPost("Hello", "World")
```

### Pagination
```bash
# cURL
curl "http://localhost:5000/api/v1/posts?page=2&per_page=20"

# Python
client.get_posts(page=2, per_page=20)

# JavaScript
await client.getPosts({ page: 2, per_page: 20 })
```

### Searching
```bash
# cURL
curl "http://localhost:5000/api/v1/posts?search=keyword"

# Python
client.search_posts("keyword")

# JavaScript
await client.searchPosts("keyword")
```

### Sorting
```bash
# cURL
curl "http://localhost:5000/api/v1/posts?sort=title&order=asc"

# Python
client.get_posts(sort="title", order="asc")

# JavaScript
await client.getPosts({ sort: "title", order: "asc" })
```

## Error Handling

All clients include basic error handling. Wrap API calls in try-catch blocks:

**Python:**
```python
try:
    post = client.create_post("Title", "Content")
except requests.exceptions.HTTPError as e:
    print(f"Error: {e}")
```

**JavaScript:**
```javascript
try {
    const post = await client.createPost("Title", "Content");
} catch (error) {
    console.error("Error:", error.response?.data || error.message);
}
```

## Response Format

All successful responses return JSON:

```json
{
  "id": 1,
  "title": "Post Title",
  "content": "Post content",
  "created_at": "2025-11-13T12:00:00",
  "updated_at": "2025-11-13T12:00:00"
}
```

Paginated responses include metadata:

```json
{
  "items": [...],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total_items": 100,
    "total_pages": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

## Further Documentation

- [API Documentation](http://localhost:5000/api/docs) - Swagger UI
- [Main README](../README.md) - Complete project documentation
