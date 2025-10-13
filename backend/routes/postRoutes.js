import express from 'express';
import { addPost } from '../controllers/postController.js';
import { validatePost } from '../middleware/validatePost.js';
// Import auth middleware if you have one
// import { protect } from '../middleware/auth.js';

const router = express.Router();

// Route to add a new post
// Add protect middleware if you have authentication set up
router.post('/', validatePost, addPost);

export default router;