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
          whileHover={{ scale: 1.05 }}
          className="flex items-center space-x-2"
        >
          <Brain className="w-8 h-8 text-primary" />
          <span className="text-xl font-bold">MindChat</span>
        </motion.div>
        
        <motion.button
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          whileHover={{ scale: 1.05, backgroundColor: "#1a1a1a" }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center space-x-2 bg-black border border-gray-800 px-4 py-2 rounded-lg hover:border-primary transition-colors"
        >
          <Home className="w-5 h-5" />
          <span>Home</span>
        </motion.button>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-6 py-20 text-center">
        <motion.h1
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-5xl md:text-7xl font-bold mb-8"
        >
          <motion.span
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ 
              duration: 0.8,
              ease: "easeOut"
            }}
            whileHover={{
              scale: 1.02,
              transition: {
                duration: 0.3,
                ease: "easeInOut"
              }
            }}
            className="block relative overflow-hidden"
          >
            <motion.span
              className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/20 to-transparent"
              initial={{ x: "-100%" }}
              whileHover={{
                x: "100%",
                transition: {
                  duration: 1.5,
                  ease: "linear",
                  repeat: Infinity
                }
              }}
            />
            Your Mental Health
          </motion.span>
          <motion.span
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ 
              delay: 0.5,
              duration: 0.8,
              ease: "easeOut"
            }}
            whileHover={{
              scale: 1.02,
              transition: {
                duration: 0.3,
                ease: "easeInOut"
              }
            }}
            className="text-primary block mt-2 relative overflow-hidden"
          >
            <motion.span
              className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/20 to-transparent"
              initial={{ x: "-100%" }}
              whileHover={{
                x: "100%",
                transition: {
                  duration: 1.5,
                  ease: "linear",
                  repeat: Infinity
                }
              }}
            />
            Companion
          </motion.span>
        </motion.h1>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ 
              delay: 1.2,
              duration: 0.8,
              ease: "easeOut"
            }}
            whileHover={{
              scale: 1.02,
              transition: {
                duration: 0.3,
                ease: "easeInOut"
              }
            }}
            className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto relative overflow-hidden"
          >
            <motion.span
              className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/20 to-transparent"
              initial={{ x: "-100%" }}
              whileHover={{
                x: "100%",
                transition: {
                  duration: 1.5,
                  ease: "linear",
                  repeat: Infinity
                }
              }}
            />
            24/7 AI-powered support for your emotional well-being. Talk to someone who understands, anytime, anywhere.
          </motion.p>
        </motion.div>

        <motion.button
          whileHover={{ scale: 1.05, backgroundColor: "#1a1a1a" }}
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
              whileHover={{ 
                scale: 1.05,
                borderColor: "#3b82f6",
                transition: { duration: 0.2 }
              }}
              className="bg-black border border-gray-800 p-6 rounded-xl hover:border-primary transition-colors"
            >
              <motion.div
                whileHover={{ scale: 1.1, rotate: 5 }}
                transition={{ duration: 0.2 }}
              >
                <feature.icon className="w-12 h-12 text-primary mb-4" />
              </motion.div>
              <motion.h3 
                className="text-xl font-semibold mb-2"
                whileHover={{ color: "#3b82f6" }}
              >
                {feature.title}
              </motion.h3>
              <motion.p 
                className="text-gray-400"
                whileHover={{ color: "#ffffff" }}
              >
                {feature.description}
              </motion.p>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;