import Roommate from '../models/Roommate.js';

// @desc    Create a new roommate post
// @route   POST /api/roommates
// @access  Private
export const addRoommate = async (req, res) => {
    try {
        const {
            title,
            images,
            description,
            placesToLive,
            region,
            onCampus,
            year
        } = req.body;

        // Create new roommate post
        const roommate = await Roommate.create({
            title,
            images,
            description,
            placesToLive,
            region,
            onCampus,
            year,
            authorId: req.user?._id, // This assumes you have user auth middleware
            status: "searching", // Default status for new posts
            favorites: 0,
            timePosted: new Date().toISOString(),
            timeUpdate: new Date().toISOString()
        });

        res.status(201).json({
            success: true,
            data: roommate
        });
    } catch (error) {
        res.status(400).json({
            success: false,
            error: error.message
        });
    }
};