# Sixt Q&A Chatbot Backend

A FastAPI backend that provides intelligent Q&A about Sixt car rental terms using Google Gemini AI.

## Features

- **Intelligent Q&A**: Uses Google Gemini to answer questions about rental terms
- **RAG (Retrieval Augmented Generation)**: Retrieves relevant terms from database and generates contextual answers
- **RESTful API**: Clean API endpoints for frontend integration
- **CORS Support**: Configured for React frontend

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Set Environment Variable

**Option A: Export in terminal**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

**Option B: Create .env file**
```bash
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

### 4. Run the Backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /ask
Ask a question about Sixt rental terms.

**Request:**
```json
{
  "question": "What is the minimum age to rent a car in the USA?"
}
```

**Response:**
```json
{
  "success": true,
  "question": "What is the minimum age to rent a car in the USA?",
  "answer": "Based on the rental terms...",
  "sources_count": 2
}
```

### GET /health
Health check endpoint.

## Database

The system uses a SQLite database (`sixt_terms.db`) containing scraped rental terms from Sixt's website.

### Database Schema
- `country`: Country name
- `vehicle_type`: Type of vehicle (Passenger vehicle, Truck)
- `rental_information`: General rental information
- `payment_information`: Payment and tariff information
- `protection_conditions`: Insurance and protection details
- `authorized_driving_areas`: Cross-border rental information
- `extras`: Additional services and extras
- `other_charges_and_taxes`: Fees and taxes
- `vat`: VAT information

## How It Works

1. **Question Processing**: User asks a question via the API
2. **Retrieval**: System searches the database for relevant rental terms
3. **Context Formation**: Relevant terms are formatted into context for the AI
4. **AI Generation**: Google Gemini generates an answer based on the context
5. **Response**: Structured response is returned to the user

## Testing

You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the minimum age to rent a car?"}'
```

## Frontend Integration

The backend is configured with CORS to work with a React frontend running on `http://localhost:3000`.

## Troubleshooting

- **API Key Error**: Make sure `GOOGLE_API_KEY` environment variable is set
- **Database Error**: Ensure `sixt_terms.db` exists and has data
- **Import Error**: Make sure all dependencies are installed in your virtual environment

---

For the frontend, see the `front-end/` directory. 