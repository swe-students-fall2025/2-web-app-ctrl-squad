// Middleware to validate post data
export const validatePost = (req, res, next) => {
    try {
        const { title, description, categories } = req.body;

        // Check if required fields exist
        if (!title || !description || !categories) {
            return res.status(400).json({
                success: false,
                error: 'Missing required fields: title, description, and category are required'
            });
        }

        // Validate title length
        if (title.length < 3 || title.length > 100) {
            return res.status(400).json({
                success: false,
                error: 'Title must be between 3 and 100 characters'
            });
        }

        // Validate description length
        if (description.length < 10 || description.length > 1000) {
            return res.status(400).json({
                success: false,
                error: 'Description must be between 10 and 1000 characters'
            });
        }

        // Validate categories
        if (!Array.isArray(categories) || categories.length === 0) {
            return res.status(400).json({
                success: false,
                error: 'At least one category is required'
            });
        }

        // Validate image URLs if they exist
        if (req.body.images) {
            if (!Array.isArray(req.body.images)) {
                return res.status(400).json({
                    success: false,
                    error: 'Images must be provided as an array'
                });
            }
        }

        // If all validations pass, proceed
        next();
    } catch (error) {
        return res.status(500).json({
            success: false,
            error: 'Error validating post data'
        });
    }
};