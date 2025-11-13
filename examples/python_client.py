"""Python client example for Blog Posts API."""
import requests
from typing import Dict, List, Optional


class BlogAPIClient:
    """Client for interacting with the Blog Posts API."""

    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize the API client.

        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            JSON response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def health_check(self) -> Dict:
        """
        Check API health status.

        Returns:
            Health status dictionary
        """
        return self._make_request('GET', '/health')

    def get_posts(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        sort: str = 'created_at',
        order: str = 'desc'
    ) -> Dict:
        """
        Get all posts with pagination and filtering.

        Args:
            page: Page number
            per_page: Items per page
            search: Search query
            sort: Sort field
            order: Sort order (asc/desc)

        Returns:
            Paginated posts response
        """
        params = {
            'page': page,
            'per_page': per_page,
            'sort': sort,
            'order': order
        }
        if search:
            params['search'] = search

        return self._make_request('GET', '/api/v1/posts', params=params)

    def get_post(self, post_id: int) -> Dict:
        """
        Get a single post by ID.

        Args:
            post_id: Post ID

        Returns:
            Post dictionary
        """
        return self._make_request('GET', f'/api/v1/posts/{post_id}')

    def create_post(self, title: str, content: str) -> Dict:
        """
        Create a new post.

        Args:
            title: Post title
            content: Post content

        Returns:
            Created post dictionary
        """
        data = {
            'title': title,
            'content': content
        }
        return self._make_request('POST', '/api/v1/posts', json=data)

    def update_post(
        self,
        post_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None
    ) -> Dict:
        """
        Update an existing post.

        Args:
            post_id: Post ID
            title: New title (optional)
            content: New content (optional)

        Returns:
            Updated post dictionary
        """
        data = {}
        if title:
            data['title'] = title
        if content:
            data['content'] = content

        return self._make_request('PUT', f'/api/v1/posts/{post_id}', json=data)

    def delete_post(self, post_id: int) -> Dict:
        """
        Delete a post.

        Args:
            post_id: Post ID

        Returns:
            Deletion confirmation
        """
        return self._make_request('DELETE', f'/api/v1/posts/{post_id}')

    def search_posts(self, query: str, page: int = 1, per_page: int = 10) -> Dict:
        """
        Search posts by query.

        Args:
            query: Search query
            page: Page number
            per_page: Items per page

        Returns:
            Search results
        """
        return self.get_posts(page=page, per_page=per_page, search=query)


def main():
    """Example usage of the Blog API client."""
    # Initialize client
    client = BlogAPIClient("http://localhost:5000")

    # Check API health
    health = client.health_check()
    print(f"API Health: {health}")

    # Create a new post
    new_post = client.create_post(
        title="My First Post via API Client",
        content="This post was created using the Python API client."
    )
    print(f"\nCreated post: {new_post}")

    # Get all posts
    posts = client.get_posts(page=1, per_page=5)
    print(f"\nTotal posts: {posts['meta']['total_items']}")
    print(f"Posts on this page: {len(posts['items'])}")

    # Search posts
    results = client.search_posts("API")
    print(f"\nSearch results: {len(results['items'])} posts found")

    # Update the post
    if new_post.get('id'):
        updated = client.update_post(
            new_post['id'],
            title="Updated Title",
            content="This content has been updated."
        )
        print(f"\nUpdated post: {updated}")

        # Delete the post
        deleted = client.delete_post(new_post['id'])
        print(f"\nDeletion result: {deleted}")


if __name__ == '__main__':
    main()
