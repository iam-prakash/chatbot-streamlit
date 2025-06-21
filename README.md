# Sixt Q&A Chatbot

A Q&A system for Sixt car rental terms using Google Gemini AI, with two interface options.

## 🚀 Quick Start (Streamlit App)

This is a self-contained application and the fastest way to get started.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
This installs Streamlit, FastAPI, sentence-transformers, and all other required packages.

### 2. Set Your Google Gemini API Key
Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey) and set it as an environment variable.

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### 3. Run the Streamlit App
```bash
streamlit run streamlit_app.py
```

That's it! Visit `http://localhost:8501` to use the chat interface. The app will pre-load the language model and handle everything automatically.

---

## 🏗️ Full Stack Setup (React + FastAPI)

This is the more advanced setup for a production-ready web application. The Streamlit app is not used in this configuration.

### 1. Backend Setup
Follow the instructions in the `backend/README.md` file to start the FastAPI server.

### 2. Frontend Setup
```bash
cd front-end
npm install
npm start
```
This will start the React development server, typically at `http://localhost:3000`.

---

## �� Project Structure

```
chat interface/
├── backend/                 # FastAPI backend logic
│   ├── app/
│   │   ├── main.py         # FastAPI server (for full-stack version)
│   │   ├── qa.py           # Gemini Q&A logic
│   │   ├── scraper.py      # Data scraper
│   │   └── db.py           # Database utilities
│   └── sixt_terms.db       # SQLite database (used by both versions)
├── front-end/              # React frontend (for full-stack version)
├── streamlit_app.py        # Standalone Streamlit chat interface
└── requirements.txt        # Python dependencies for both versions
```

## 🎯 Features

- **Dual Interface**: Streamlit for quick testing, React for production
- **Intelligent Q&A**: Google Gemini-powered responses
- **RAG System**: Retrieval Augmented Generation for accurate answers
- **Real-time Chat**: Conversation history and context
- **Database Integration**: SQLite with scraped rental terms

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key

### Backend URL
- Default: `http://localhost:8000`
- Change in `streamlit_app.py` if needed

## 🚀 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Set environment variables
4. Deploy!

### Full Stack
- Backend: Deploy FastAPI to your preferred platform
- Frontend: Deploy React to Vercel/Netlify

## 🧪 Testing

### Test Gemini Integration
```bash
cd backend
python test_gemini.py
```

### Test API
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the minimum age to rent a car?"}'
```

## 📝 Notes

- **Streamlit**: Perfect for prototyping and demos
- **Full Stack**: Better for production and customization
- **Database**: Currently empty - run scraper to populate with real data 