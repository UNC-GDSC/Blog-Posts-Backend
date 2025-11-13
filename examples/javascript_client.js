/**
 * JavaScript/Node.js client example for Blog Posts API
 * Requires: npm install axios
 */

const axios = require('axios');

class BlogAPIClient {
    constructor(baseURL = 'http://localhost:5000') {
        this.client = axios.create({
            baseURL: baseURL,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    async healthCheck() {
        const response = await this.client.get('/health');
        return response.data;
    }

    async getPosts(params = {}) {
        const defaultParams = {
            page: 1,
            per_page: 10,
            sort: 'created_at',
            order: 'desc'
        };
        const response = await this.client.get('/api/v1/posts', {
            params: { ...defaultParams, ...params }
        });
        return response.data;
    }

    async getPost(postId) {
        const response = await this.client.get(`/api/v1/posts/${postId}`);
        return response.data;
    }

    async createPost(title, content) {
        const response = await this.client.post('/api/v1/posts', {
            title,
            content
        });
        return response.data;
    }

    async updatePost(postId, data) {
        const response = await this.client.put(`/api/v1/posts/${postId}`, data);
        return response.data;
    }

    async deletePost(postId) {
        const response = await this.client.delete(`/api/v1/posts/${postId}`);
        return response.data;
    }

    async searchPosts(query, page = 1, perPage = 10) {
        return await this.getPosts({
            search: query,
            page,
            per_page: perPage
        });
    }
}

// Example usage
async function main() {
    const client = new BlogAPIClient('http://localhost:5000');

    try {
        // Health check
        console.log('Checking API health...');
        const health = await client.healthCheck();
        console.log('Health:', health);

        // Create a post
        console.log('\nCreating a new post...');
        const newPost = await client.createPost(
            'My Post from JavaScript',
            'This post was created using the JavaScript client.'
        );
        console.log('Created:', newPost);

        // Get all posts
        console.log('\nFetching all posts...');
        const posts = await client.getPosts({ page: 1, per_page: 5 });
        console.log(`Total posts: ${posts.meta.total_items}`);
        console.log(`Posts on page: ${posts.items.length}`);

        // Search posts
        console.log('\nSearching posts...');
        const searchResults = await client.searchPosts('JavaScript');
        console.log(`Found ${searchResults.items.length} posts`);

        // Update post
        if (newPost.id) {
            console.log('\nUpdating post...');
            const updated = await client.updatePost(newPost.id, {
                title: 'Updated Title',
                content: 'Updated content from JavaScript'
            });
            console.log('Updated:', updated);

            // Delete post
            console.log('\nDeleting post...');
            const deleted = await client.deletePost(newPost.id);
            console.log('Deleted:', deleted);
        }
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

// Run if executed directly
if (require.main === module) {
    main();
}

module.exports = BlogAPIClient;
