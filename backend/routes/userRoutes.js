import express from 'express';
import { getUserProfile, updateUserProfile } from '../controllers/userController.js';
import { validateUserUpdate } from '../middleware/validateUserUpdate.js';
// Import auth middleware when ready
// import { protect } from '../middleware/auth.js';

const router = express.Router();

// User profile routes
router.route('/profile')
    .get(getUserProfile)    // Add protect middleware when ready
    .put(validateUserUpdate, updateUserProfile); // Add protect middleware when ready

export default router;