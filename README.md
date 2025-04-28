# 🧠 Mental Health Chatbot Project

This project consists of two main components:
1. 🤖 A Python-based chatbot using Streamlit for mental health recommendations
2. 🌐 A web application with React frontend and Express backend

## ✨ Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) 🐳
- [Node.js](https://nodejs.org/) (v18 or higher) 📦
- [Python](https://www.python.org/downloads/) (v3.8 or higher) 🐍
- [MongoDB](https://www.mongodb.com/try/download/community) (if running without Docker) 🍃

## 📁 Project Structure

```
Directory structure:
└── trahulprabhu38-project-1/
    ├── README.md
    ├── Docker-compose.yaml
    ├── .gitIgnore
    ├── landingPage/
    │   ├── .DS_Store
    │   ├── client/
    │   │   ├── Dockerfile
    │   │   ├── index.html
    │   │   ├── package-lock.json
    │   │   ├── package.json
    │   │   ├── postcss.config.js
    │   │   ├── tailwind.config.js
    │   │   ├── vite.config.js
    │   │   ├── .env
    │   │   ├── .gitignore
    │   │   └── src/
    │   │       ├── App.jsx
    │   │       ├── index.css
    │   │       ├── main.jsx
    │   │       └── components/
    │   │           └── Auth.jsx
    │   └── server/
    │       ├── Dockerfile
    │       ├── package-lock.json
    │       ├── package.json
    │       ├── server copy.js
    │       ├── server.js
    │       ├── .env
    │       └── .gitignore
    └── Medbot-Project1/
        ├── auth_helper.py
        ├── chatbot.py
        ├── db_handler.py
        ├── Dockerfile
        ├── encryption.py
        ├── main.py
        ├── mental_health_recommendations.json
        ├── my_dataset.csv
        ├── recommendation_system.py
        ├── requirements.txt
        ├── resources.py
        ├── sentiment.py
        ├── vid.py
        ├── .DS_Store
        └── .gitignore

```

## 🔑 Environment Variables

Create `.env` files in the following directories:

### For chatbot/
```
GROQ_API_KEY=your_groq_api_key
MONGO_URI=mongodb://localhost:27017/mydb
ENCRYPTION_KEY=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
ANONYMIZATION_SALT=your_secure_salt_here
JWT_SECRET=your_jwt_secret
DEV_MODE=false
```

### For web/server/
```
MONGODB_URI=mongodb://localhost:27017/mydb
JWT_SECRET=your_jwt_secret
PORT=5001
```

## 🐳 Running with Docker (Recommended)

The easiest way to run all components together is using Docker:

1. Make sure Docker and Docker Compose are installed
2. Navigate to the project root directory
3. Run:
```bash
docker-compose up
```

This will start:
- The React frontend at http://localhost:5173
- The Express backend at http://localhost:5001
- The Streamlit chatbot at http://localhost:8501
- MongoDB at localhost:27017

## 🚀 Running Components Individually

### Chatbot (Python/Streamlit)

1. Navigate to the chatbot directory:
```bash
cd chatbot
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:
```bash
streamlit run main.py
```

The chatbot will be available at http://localhost:8501

### Web Application

#### Frontend

1. Navigate to the client directory:
```bash
cd web/client
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

#### Backend

1. Navigate to the server directory:
```bash
cd web/server
```

2. Install dependencies:
```bash
npm install
```

3. Run the server:
```bash
npm run dev
```

The backend API will be available at http://localhost:5001

## ✨ Features

- 💬 Mental health chatbot with sentiment analysis
- 🔐 User authentication and encrypted data storage
- 💊 Mental health recommendations based on user input
- 🖥️ Interactive web interface
- 📊 Data visualization for mental health insights
- 🔒 Privacy-focused design with data anonymization

## 🛠️ Tech Stack

### Chatbot
- **Streamlit** (v1.x): Interactive Python web app framework for the chatbot interface
- **LangChain** & **LangChain Community**: Framework for developing applications powered by language models
- **OpenAI/Groq**: AI model integration for natural language processing
- **NLTK**: For sentiment analysis and text processing
- **PyMongo**: MongoDB client for Python to handle database operations
- **Pycryptodome**: For encryption and data protection
- **Pandas & NumPy**: Data manipulation and analysis
- **Plotly & Matplotlib**: Data visualization
- **PyJWT**: JSON Web Token implementation for authentication
- **Scikit-learn**: For machine learning algorithms used in recommendations
- **Transformers**: Hugging Face's transformers for NLP tasks

### Web Application
- **React 18**: UI library with hooks for state management
- **Vite**: Next-generation frontend tooling for faster development
- **React Router 7**: Client-side routing
- **Framer Motion**: Animation library for React
- **Axios**: Promise-based HTTP client for API requests
- **TailwindCSS**: Utility-first CSS framework
- **Express.js**: Web framework for Node.js
- **MongoDB**: NoSQL database for data storage
- **Mongoose**: MongoDB object modeling for Node.js
- **JWT**: JSON Web Token for authentication
- **bcryptjs**: Library for password hashing
- **Cors**: Middleware for handling Cross-Origin Resource Sharing

### DevOps
- **Docker & Docker Compose**: Containerization and orchestration
- **Nodemon**: Development tool for Node.js applications

## 👨‍💻 Contributors

<a href="https://github.com/trahulprabhu38/project-1/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=trahulprabhu38/project-1" />
</a>



