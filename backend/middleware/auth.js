import jwt from 'jsonwebtoken';
import User from '../models/User.js';

export const protect = async (req, res, next) => {
    let token;
    
    if (req.session.userId) {
        try {
            const user = await User.findById(req.session.userId).select('-password');
            if (!user) {
                return res.status(401).json({ error: "Not authorized, no user found" });
            }
            req.user = user;
            next();
        } catch (error) {
            console.error('Session auth error:', error);
            return res.status(401).json({ error: "Not authorized, session invalid" });
        }
    } else {
        res.status(401).json({ error: "Not authorized, no session" });
    }
};