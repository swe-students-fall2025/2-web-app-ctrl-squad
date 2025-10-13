import Post from '../models/Post.js';

// @desc    Create a new post
// @route   POST /api/posts
// @access  Private
export const addPost = async (req, res) => {
    try {
        const {
            title,
            images,
            description,
            exchange_type,
            condition,
            location,
            categories
        } = req.body;

        // Create new post
        const post = await Post.create({
            title,
            images,
            description,
            exchange_type,
            condition,
            location,
            categories,
            author_id: req.user._id, // This assumes you have user auth middleware
            status: "available", // Default status for new posts
            favorites: 0,
            time_updated: new Date(),
        });

        res.status(201).json({
            success: true,
            data: post
        });
    } catch (error) {
        res.status(400).json({
            success: false,
            error: error.message
        });
    }
};