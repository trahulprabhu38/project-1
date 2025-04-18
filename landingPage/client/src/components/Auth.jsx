import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';

// Create axios instance with default config
const api = axios.create({
    baseURL: 'http://localhost:5001',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    }
});

const Auth = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const payload = isLogin 
                ? { username, password }
                : { username, password, name };

            const response = await api.post(`/api/${isLogin ? "login" : "signup"}`, payload);

            if (response.data.token) {
                // Store token in localStorage
                localStorage.setItem("token", response.data.token);
                
                // Redirect to Streamlit app with token and JWT secret
                const streamlitUrl = `http://localhost:8501?token=${response.data.token}&jwt_secret=${response.data.jwtSecret}`;
                window.location.href = streamlitUrl;
            } else {
                setError("Authentication failed");
            }
        } catch (err) {
            console.error("Auth error:", err);
            setError(err.response?.data?.error || "An error occurred");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full max-w-md p-8 bg-gray-900 rounded-lg shadow-lg"
            >
                <div className="text-center mb-8">
                    <h2 className="text-2xl font-bold mb-2">{isLogin ? "Welcome Back" : "Create Account"}</h2>
                    <p className="text-gray-400">
                        {isLogin ? "Sign in to continue" : "Join us to get started"}
                    </p>
                </div>

                {error && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-3 rounded-lg mb-4"
                    >
                        {error}
                    </motion.div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    {!isLogin && (
                        <div>
                            <label className="block text-gray-300 mb-2">Full Name</label>
                            <input
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-primary"
                                required={!isLogin}
                            />
                        </div>
                    )}

                    <div>
                        <label className="block text-gray-300 mb-2">Username</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-primary"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-gray-300 mb-2">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-primary"
                            required
                        />
                    </div>

                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        type="submit"
                        disabled={loading}
                        className="w-full bg-primary hover:bg-primary-dark text-white py-3 rounded-lg font-semibold transition-colors"
                    >
                        {loading ? "Loading..." : (isLogin ? "Login" : "Sign Up")}
                    </motion.button>
                </form>

                <div className="mt-6 text-center">
                    <button
                        onClick={() => {
                            setIsLogin(!isLogin);
                            setError('');
                            setName('');
                        }}
                        className="text-gray-400 hover:text-white transition-colors"
                    >
                        {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Login"}
                    </button>
                </div>
            </motion.div>
        </div>
    );
};

export default Auth; 