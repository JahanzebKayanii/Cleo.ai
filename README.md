# Cleo Voice AI

An AI-powered voice receptionist for service businesses. Cleo answers inbound phone calls, understands customer intent, retrieves relevant business knowledge using RAG, and performs actions like booking appointments and logging call history.

Built as a production-grade portfolio project demonstrating full-stack AI engineering.

---

## Demo

**Test business:** Apex Home Services — a fictional HVAC, plumbing, and electrical company based in Austin, TX.

**What Cleo can do on a live call:**
- Answer questions about services, pricing, and availability using company documents
- Book appointments with conflict detection
- Recognize returning callers
- Log full transcripts and conversation summaries to a database

---

## Architecture

```
Caller
  ↓
Twilio (inbound call)
  ↓
Deepgram (speech-to-text)
  ↓
FastAPI Backend
  ↓
Qdrant (vector search) ← Company knowledge documents
  ↓
Claude API (LLM reasoning + response generation)
  ↓
Twilio (text-to-speech → caller)
  ↓
PostgreSQL (call logs, transcripts, appointments, customers)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| LLM | Anthropic Claude API |
| Embeddings | Voyage AI (voyage-3, 1024 dimensions) |
| Vector DB | Qdrant |
| Relational DB | PostgreSQL |
| Voice | Twilio Voice API |
| Speech-to-Text | Deepgram (nova-2) |
| Text-to-Speech | Twilio Alice (ElevenLabs ready — upgrade path) |
| Infrastructure | Docker, Docker Compose |

---

## Features

### RAG Knowledge System
- Upload plain text or markdown documents via API
- Automatically chunks, embeds, and stores in Qdrant
- Semantic search retrieves relevant context per query
- Claude answers grounded in real business data — no hallucination

### Voice Pipeline
- Inbound calls handled via Twilio webhook
- Caller speech recorded and transcribed by Deepgram nova-2
- Claude generates a response using RAG context
- Response spoken back to caller via Twilio

### Appointment Booking
- Apex-style 2-hour arrival windows (8am–6pm)
- Conflict detection prevents double-booking
- Appointments stored in PostgreSQL with customer linkage

### Customer Management
- Callers automatically identified by phone number
- Returning customers recognised without re-registration
- Full call transcripts saved per customer

### Call Logging
- Every call stored with transcript, status, and timestamps
- Conversation history maintained within each call session
- Call ended event triggers cleanup

---

## Project Structure

```
cleo/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── call.py          # Twilio webhooks
│   │   │   ├── conversation.py  # Claude conversation endpoint
│   │   │   ├── documents.py     # RAG document upload + search
│   │   │   ├── appointments.py  # Booking endpoints
│   │   │   ├── customers.py     # Customer management
│   │   │   └── health.py        # Health check
│   │   ├── services/
│   │   │   ├── conversation_service.py  # Claude + RAG pipeline
│   │   │   ├── document_service.py      # Chunking + embedding
│   │   │   ├── stt_service.py           # Deepgram STT
│   │   │   ├── tts_service.py           # ElevenLabs TTS (upgrade path)
│   │   │   ├── appointment_service.py   # Booking logic
│   │   │   ├── customer_service.py      # Customer lookup
│   │   │   └── call_service.py          # Call lifecycle
│   │   ├── models/              # SQLAlchemy models
│   │   └── core/                # Config, DB, Qdrant setup
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
└── apex_home_services.txt       # Test knowledge base document
```

---

## Getting Started

### Prerequisites
- Docker Desktop
- ngrok (for local Twilio webhook tunneling)
- Accounts: Twilio, Deepgram, Anthropic, Voyage AI

### 1. Clone and configure

```bash
git clone <your-repo-url>
cd cleo
cp .env.example .env
```

Fill in your API keys in `.env`.

### 2. Start the stack

```bash
docker compose up --build
```

This starts PostgreSQL, Qdrant, and the FastAPI backend. Tables and vector collections are created automatically on first run.

### 3. Upload a knowledge document

```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@apex_home_services.txt"
```

### 4. Expose your local server

```bash
ngrok http 8000
```

### 5. Configure Twilio

In your Twilio phone number settings:
- **Voice webhook:** `https://<your-ngrok-url>/call/incoming` (HTTP POST)
- **Status callback:** `https://<your-ngrok-url>/call/status` (HTTP POST)

### 6. Call your Twilio number

Cleo will answer, transcribe your speech with Deepgram, search the knowledge base, and respond using Claude.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | System health check |
| POST | `/documents/upload` | Upload a knowledge document |
| GET | `/documents/search?q=` | Semantic search across documents |
| POST | `/conversation/message` | Chat with Cleo (no voice) |
| POST | `/call/incoming` | Twilio inbound call webhook |
| POST | `/call/transcribe` | Deepgram transcription + Claude response |
| POST | `/call/status` | Twilio call status callback |
| POST | `/appointments/create` | Book an appointment |
| GET | `/appointments/slots?date=` | Get available time slots |
| GET | `/appointments/{id}` | Get appointment by ID |
| POST | `/customers/` | Create or find a customer |
| GET | `/customers/{id}` | Get customer by ID |

---

## Known Limitations

- **Response latency (~6 seconds):** The current architecture records the caller's speech, uploads to Twilio, downloads, then sends to Deepgram. The fix is real-time WebSocket streaming (Phase 2).
- **ElevenLabs TTS:** Requires a paid ElevenLabs plan. Currently using Twilio's built-in Alice voice. ElevenLabs integration is built and ready — just needs a valid API key.
- **No live calendar:** Appointment availability is based on database slots, not a real calendar integration.

---

## Roadmap (Phase 2)

- [ ] Real-time voice via Twilio Media Streams + Deepgram WebSocket (reduces latency to ~2-3s)
- [ ] ElevenLabs natural voice (on paid plan)
- [ ] LangGraph multi-agent system (RAG agent, booking agent, orchestrator)
- [ ] Call summary generation using Claude after each call ends
- [ ] Admin dashboard (Next.js) — view calls, bookings, customers
- [ ] CRM integration (HubSpot/Salesforce)
- [ ] MCP tool server architecture
- [ ] Multi-tenant SaaS (multiple businesses)
- [ ] AWS EC2 deployment

---

## Environment Variables

```env
# Database
POSTGRES_USER=cleo
POSTGRES_PASSWORD=cleo_pass
POSTGRES_DB=cleo_db

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=cleo_docs

# AI
ANTHROPIC_API_KEY=your_key
VOYAGE_API_KEY=your_key

# Voice
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
DEEPGRAM_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=your_voice_id

# App
BASE_URL=https://your-ngrok-or-domain.com
```
