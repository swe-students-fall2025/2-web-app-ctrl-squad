import User from '../models/User.js';
import bcrypt from 'bcrypt';

// @desc    Get user profile
// @route   GET /api/users/profile
// @access  Private
export const getUserProfile = async (req, res) => {
    try {
        const user = await User.findById(req.user._id).select('-password');
        if (!user) {
            return res.status(404).json({
                success: false,
                error: 'User not found'
            });
        }

        res.json({
            success: true,
            data: user
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: 'Error retrieving user profile'
        });
    }
};

// @desc    Update user profile
// @route   PUT /api/users/profile
// @access  Private
export const updateUserProfile = async (req, res) => {
    try {
        const user = await User.findById(req.user._id);
        if (!user) {
            return res.status(404).json({
                success: false,
                error: 'User not found'
            });
        }

        // Update fields if they are provided
        user.account_name = req.body.account_name || user.account_name;
        user.email = req.body.email || user.email;
        user.nyu_id = req.body.nyu_id || user.nyu_id;
        user.bio = req.body.bio || user.bio;
        
        // If password is being updated
        if (req.body.password) {
            const salt = await bcrypt.genSalt(10);
            user.password = await bcrypt.hash(req.body.password, salt);
        }

        // Save updated user
        const updatedUser = await user.save();

        res.json({
            success: true,
            data: {
                _id: updatedUser._id,
                account_name: updatedUser.account_name,
                email: updatedUser.email,
                nyu_id: updatedUser.nyu_id,
                bio: updatedUser.bio
            }
        });
    } catch (error) {
        res.status(400).json({
            success: false,
            error: error.message
        });
    }
};