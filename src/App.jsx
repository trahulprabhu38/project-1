import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Home, MessageCircle, Shield, Heart, Sparkles, Zap } from 'lucide-react';

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center space-x-2"
        >
          <Brain className="w-8 h-8 text-primary" />
          <span className="text-xl font-bold">MindChat</span>
        </motion.div>
        
        <motion.button
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center space-x-2 bg-black border border-gray-800 px-4 py-2 rounded-lg hover:border-primary transition-colors"
        >
          <Home className="w-5 h-5" />
          <span>Home</span>
        </motion.button>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-6 py-20 text-center">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-5xl md:text-7xl font-bold mb-8"
        >
          Your Mental Health
          <span className="text-primary block mt-2">Companion</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto"
        >
          24/7 AI-powered support for your emotional well-being. Talk to someone who understands, anytime, anywhere.
        </motion.p>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="bg-primary hover:bg-primary-dark text-white px-8 py-4 rounded-full text-xl font-semibold transition-colors flex items-center space-x-2 mx-auto"
        >
          <MessageCircle className="w-6 h-6" />
          <span>Start Chatting Now</span>
        </motion.button>
      </main>

      {/* Features Grid */}
      <section className="container mx-auto px-6 py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {[
            {
              icon: Shield,
              title: "Safe & Confidential",
              description: "Your conversations are private and secure, always."
            },
            {
              icon: Heart,
              title: "Empathetic Support",
              description: "Experience understanding without judgment, 24/7."
            },
            {
              icon: Sparkles,
              title: "AI-Powered Insights",
              description: "Get personalized guidance based on your needs."
            },
            {
              icon: Zap,
              title: "Instant Response",
              description: "No waiting time, get help when you need it most."
            }
          ].map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-black border border-gray-800 p-6 rounded-xl hover:border-primary transition-colors"
            >
              <feature.icon className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;