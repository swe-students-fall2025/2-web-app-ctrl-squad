// Middleware to validate roommate post data
export const validateRoommatePost = (req, res, next) => {
    try {
        const { title, description, placesToLive, region, year } = req.body;
        const errors = [];

        // Check required fields
        if (!title) errors.push('Title is required');
        if (!description) errors.push('Description is required');
        if (!placesToLive) errors.push('Places to live preference is required');
        if (!region) errors.push('Region is required');
        if (!year) errors.push('Year is required');

        // Validate title length
        if (title && (title.length < 3 || title.length > 100)) {
            errors.push('Title must be between 3 and 100 characters');
        }

        // Validate description length
        if (description && (description.length < 10 || description.length > 1000)) {
            errors.push('Description must be between 10 and 1000 characters');
        }

        // Validate year
        if (year && (isNaN(year) || year < 1 || year > 4)) {
            errors.push('Year must be a number between 1 and 4');
        }

        // Validate images if they exist
        if (req.body.images && !Array.isArray(req.body.images)) {
            errors.push('Images must be provided as an array');
        }

        // Check if there are any validation errors
        if (errors.length > 0) {
            return res.status(400).json({
                success: false,
                error: errors.join(', ')
            });
        }

        // If all validations pass, proceed
        next();
    } catch (error) {
        return res.status(500).json({
            success: false,
            error: 'Error validating roommate post data'
        });
    }
};