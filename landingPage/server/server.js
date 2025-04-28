const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
require('dotenv').config();

const app = express();

//cors
app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true
}));

app.use(express.json());

const connectToDatabase = async () => {
    try {
        await mongoose.connect(process.env.MONGODB_URI ||"mongodb://localhost:27017/medbot", {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        console.log('MongoDB Connected');
    } catch (err) {
        console.error('MongoDB Connection Error:', err);
    }
};

connectToDatabase();


// User Schema
const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    name: { type: String, required: true },
    password: { type: String, required: true },
    createdAt: { type: Date, default: Date.now }
});

// Create new username index
userSchema.index({ username: 1 }, { unique: true });

const User = mongoose.model('User', userSchema);

// Chat Schema
const chatSchema = new mongoose.Schema({
    userId: { type: String, required: true },
    title: { type: String, required: true },
    messages: [{
        role: { type: String, required: true },
        content: { type: String, required: true },
        timestamp: { type: Date, default: Date.now }
    }],
    createdAt: { type: Date, default: Date.now }
});

const Chat = mongoose.model('Chat', chatSchema);

// JWT Secret
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

// Middleware to verify JWT token
const verifyToken = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
        return res.status(401).json({ error: 'No token provided' });
    }

    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        req.userId = decoded.userId;
        next();
    } catch (error) {
        return res.status(401).json({ error: 'Invalid token' });
    }
};

// Signup endpoint
app.post('/api/signup', async (req, res) => {
    try {
        const { username, password, name } = req.body;
        
        // Check if user already exists
        const existingUser = await User.findOne({ username });
        if (existingUser) {
            return res.status(400).json({ error: "Username already exists" });
        }
        
        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);
        
        // Create new user
        const user = new User({
            username,
            name,
            password: hashedPassword
        });
        
        await user.save();
        
        // Generate JWT token
        const token = jwt.sign(
            { userId: user._id.toString() },
            JWT_SECRET,
            { expiresIn: "24h" }
        );
        
        res.status(201).json({
            token,
            userId: user._id.toString(),
            jwtSecret: JWT_SECRET,
            message: "User created successfully"
        });
    } catch (error) {
        console.error("Signup error:", error);
        res.status(500).json({ error: "Error creating user" });
    }
});

// Login endpoint
app.post('/api/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        
        // Find user
        const user = await User.findOne({ username });
        if (!user) {
            return res.status(401).json({ error: "Invalid credentials" });
        }
        
        // Verify password
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.status(401).json({ error: "Invalid credentials" });
        }
        
        // Generate JWT token
        const token = jwt.sign(
            { userId: user._id.toString() },
            JWT_SECRET,
            { expiresIn: "24h" }
        );
        
        res.json({
            token,
            userId: user._id.toString(),
            jwtSecret: JWT_SECRET,
            message: "Login successful"
        });
    } catch (error) {
        console.error("Login error:", error);
        res.status(500).json({ error: "Error logging in" });
    }
});

// Get user's chats
app.get('/api/chats', verifyToken, async (req, res) => {
    try {
        const chats = await Chat.find({ userId: req.userId })
            .sort({ createdAt: -1 })
            .select('_id title createdAt');
        res.json(chats);
    } catch (error) {
        console.error('Error fetching chats:', error);
        res.status(500).json({ error: 'Error fetching chats' });
    }
});

// Create new chat
app.post('/api/chats', verifyToken, async (req, res) => {
    try {
        const chat = new Chat({
            userId: req.userId,
            title: req.body.title || 'New Chat',
            messages: []
        });
        await chat.save();
        res.status(201).json(chat);
    } catch (error) {
        console.error('Error creating chat:', error);
        res.status(500).json({ error: 'Error creating chat' });
    }
});

// Get specific chat
app.get('/api/chats/:chatId', verifyToken, async (req, res) => {
    try {
        const chat = await Chat.findOne({
            _id: req.params.chatId,
            userId: req.userId
        });
        if (!chat) {
            return res.status(404).json({ error: 'Chat not found' });
        }
        res.json(chat);
    } catch (error) {
        console.error('Error fetching chat:', error);
        res.status(500).json({ error: 'Error fetching chat' });
    }
});

// Update chat messages
app.put('/api/chats/:chatId', verifyToken, async (req, res) => {
    try {
        const chat = await Chat.findOneAndUpdate(
            { _id: req.params.chatId, userId: req.userId },
            { $set: { messages: req.body.messages } },
            { new: true }
        );
        if (!chat) {
            return res.status(404).json({ error: 'Chat not found' });
        }
        res.json(chat);
    } catch (error) {
        console.error('Error updating chat:', error);
        res.status(500).json({ error: 'Error updating chat' });
    }
});

// Delete chat
app.delete('/api/chats/:chatId', verifyToken, async (req, res) => {
    try {
        const chat = await Chat.findOneAndDelete({
            _id: req.params.chatId,
            userId: req.userId
        });
        if (!chat) {
            return res.status(404).json({ error: 'Chat not found' });
        }
        res.json({ message: 'Chat deleted successfully' });
    } catch (error) {
        console.error('Error deleting chat:', error);
        res.status(500).json({ error: 'Error deleting chat' });
    }
});

app.get('/',(req,res)=>{
    res.send("hey its working!")
})

const HOST = '0.0.0.0'; 

const PORT = process.env.PORT || 5001;
app.listen(PORT,HOST, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(" ------------------------ this is working  ------------------------");
}); 