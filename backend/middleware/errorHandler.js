// Error handling middleware
export const errorHandler = (err, req, res, next) => {
    console.error('Error:', err);

    // Check if headers have already been sent
    if (res.headersSent) {
        return next(err);
    }

    // Mongoose validation error
    if (err.name === 'ValidationError') {
        return res.status(400).json({
            success: false,
            error: Object.values(err.errors).map(val => val.message).join(', ')
        });
    }

    // Mongoose duplicate key error
    if (err.code === 11000) {
        return res.status(400).json({
            success: false,
            error: 'Duplicate field value entered'
        });
    }

    // Default to 500 server error
    return res.status(500).json({
        success: false,
        error: 'Server Error'
    });
};