import express from 'express';
import { addRoommate } from '../controllers/roommateController.js';
import { validateRoommatePost } from '../middleware/validateRoommatePost.js';
// Import auth middleware if you have one
// import { protect } from '../middleware/auth.js';

const router = express.Router();

// Route to add a new roommate post
// Add protect middleware if you have authentication set up
router.post('/', validateRoommatePost, addRoommate);

export default router;