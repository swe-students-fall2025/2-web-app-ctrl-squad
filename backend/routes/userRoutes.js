import express from 'express';
import { getUserProfile, updateUserProfile } from '../controllers/userController.js';
import { validateUserUpdate } from '../middleware/validateUserUpdate.js';
import { protect } from '../middleware/auth.js';

const router = express.Router();

// User profile routes
router.route('/profile')
    .get(protect, getUserProfile)
    .put(protect, validateUserUpdate, updateUserProfile);

export default router;