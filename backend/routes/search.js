const express = require('express');
const router = express.Router();
const Post = require('../models/Post');

// GET /api/search?q=query
router.get('/', async (req, res) => {
    try {
        const query = req.query.q;
        
        if (!query) {
            return res.status(400).json({
                success: false,
                error: 'Search query is required'
            });
        }

        // Create a case-insensitive regex pattern
        const searchRegex = new RegExp(query, 'i');

        // Search in title and description
        const posts = await Post.find({
            $or: [
                { title: searchRegex },
                { description: searchRegex }
            ]
        })
        .populate('author', 'username') // Get author name
        .sort({ createdAt: -1 }) // Sort by newest first
        .limit(20); // Limit results to prevent overwhelming response

        const results = posts.map(post => ({
            _id: post._id,
            title: post.title,
            imageUrl: post.imageUrl,
            author_name: post.author ? post.author.username : 'Anonymous',
            favorites: post.favorites || [],
            createdAt: post.createdAt
        }));

        res.json({
            success: true,
            results
        });

    } catch (error) {
        console.error('Search error:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to perform search'
        });
    }
});

module.exports = router;