# 🧠 Mental Health Chatbot Project

This project consists of two main components:
1. 🤖 A Python-based chatbot using Streamlit for mental health recommendations
2. 🌐 A web application with React frontend and Express backend


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


### Chatbot (Streamlit)

```bash
#1. Navigate to the chatbot directory:
cd chatbot

#2. Create a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies:
pip install -r requirements.txt

# 4. Run the Streamlit app:
streamlit run main.py

# The chatbot will be available at http://localhost:8501
```




### Web Application

#### Frontend

```bash
# 1. Navigate to the client directory:
cd web/client

# 2. Install dependencies:
npm install

# 3. Run the development server:
npm run dev

# The frontend will be available at http://localhost:5173
```



#### Backend

```bash
# 1. Navigate to the server directory:
cd web/server

# 2. Install dependencies:
npm install

# 3. Run the server:
npm run dev

# The backend API will be available at http://localhost:5001
```




## ✨ Features

- 💬 Mental health chatbot with sentiment analysis
- 🔐 User authentication and encrypted data storage
- 💊 Mental health recommendations based on user input
- 🖥️ Interactive web interface
- 📊 Data visualization for mental health insights
- 🔒 Privacy-focused design with data anonymization

## 🛠️ Tech Stack

### Chatbot
- **Streamlit** 
- **LangChain** 
- **LangChain Community models**
- **OpenAI/Groq**
- **NLTK**
- **PyMongo**
- **Pycryptodome**
- **Pandas & NumPy**
- **Plotly & Matplotlib**
- **PyJWT**
- **Scikit-learn**
- **Transformers**

### Web Application
- **React 18**
- **Axios**
- **Express.js**
- **MongoDB**
- **JWT**
- **bcryptjs**
- **Cors**

### DevOps
- **Docker & Docker Compose**
- **Nodemon**

## 👨‍💻 Contributors

<a href="https://github.com/trahulprabhu38/project-1/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=trahulprabhu38/project-1" />
</a>

  _      _      _
>(.)__ <(.)__ =(.)__
 (___/  (___/  (___/





