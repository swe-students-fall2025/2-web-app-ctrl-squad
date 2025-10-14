// Middleware to validate user profile updates
export const validateUserUpdate = (req, res, next) => {
    try {
        const { email, account_name, nyu_id, password } = req.body;
        const errors = [];

        // Validate email if provided
        if (email) {
            const emailRegex = /^[^\s@]+@nyu\.edu$/;
            if (!emailRegex.test(email)) {
                errors.push('Email must be a valid NYU email address');
            }
        }

        // Validate account name if provided
        if (account_name) {
            if (account_name.length < 2 || account_name.length > 50) {
                errors.push('Account name must be between 2 and 50 characters');
            }
        }

        // Validate NYU ID if provided
        if (nyu_id) {
            const nyuIdRegex = /^N\d{7}$/;
            if (!nyuIdRegex.test(nyu_id)) {
                errors.push('NYU ID must be in the format N1234567');
            }
        }

        // Validate password if provided
        if (password) {
            if (password.length < 6) {
                errors.push('Password must be at least 6 characters long');
            }
        }

        // Validate bio if provided
        if (req.body.bio && req.body.bio.length > 280) {
            errors.push('Bio must not exceed 280 characters');
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
            error: 'Error validating user data'
        });
    }
};