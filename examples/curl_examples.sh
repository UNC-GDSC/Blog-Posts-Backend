#!/bin/bash
# Curl examples for Blog Posts API

BASE_URL="http://localhost:5000"

echo "=== Blog Posts API - cURL Examples ==="
echo ""

# Health Check
echo "1. Health Check"
curl -X GET "${BASE_URL}/health" | jq '.'
echo -e "\n"

# Ping
echo "2. Ping"
curl -X GET "${BASE_URL}/ping" | jq '.'
echo -e "\n"

# Get all posts
echo "3. Get All Posts (paginated)"
curl -X GET "${BASE_URL}/api/v1/posts?page=1&per_page=10" | jq '.'
echo -e "\n"

# Get single post
echo "4. Get Post by ID"
curl -X GET "${BASE_URL}/api/v1/posts/1" | jq '.'
echo -e "\n"

# Create a new post
echo "5. Create New Post"
curl -X POST "${BASE_URL}/api/v1/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Post from cURL",
    "content": "This is a test post created using cURL."
  }' | jq '.'
echo -e "\n"

# Update a post
echo "6. Update Post"
curl -X PUT "${BASE_URL}/api/v1/posts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content from cURL."
  }' | jq '.'
echo -e "\n"

# Search posts
echo "7. Search Posts"
curl -X GET "${BASE_URL}/api/v1/posts?search=test&page=1&per_page=5" | jq '.'
echo -e "\n"

# Sort posts
echo "8. Sort Posts by Title (ascending)"
curl -X GET "${BASE_URL}/api/v1/posts?sort=title&order=asc&per_page=5" | jq '.'
echo -e "\n"

# Delete a post
echo "9. Delete Post"
curl -X DELETE "${BASE_URL}/api/v1/posts/1" | jq '.'
echo -e "\n"

echo "=== Examples Complete ==="
