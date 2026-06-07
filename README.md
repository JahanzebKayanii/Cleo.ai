# Cleo — AI Voice Receptionist

Cleo answers every inbound call, collects job details, books appointments, and syncs everything to your CRM, calendar, and field service tools — automatically. Built for HVAC, plumbing, electrical, and home service businesses.

Part of the [CleoVoice](https://cleovoice.com) product suite.

---

## What Cleo Does

- **Answers every call** — no hold music, no voicemail. Cleo picks up instantly and greets callers by name if they're returning customers.
- **Books appointments** — checks real availability, presents open slots, confirms the booking, and prevents double-booking.
- **Syncs to your tools** — job lands in Google Calendar, contact created in HubSpot, Jobber, Housecall Pro, or QuickBooks within seconds of the call ending.
- **Sends SMS confirmations** — caller gets a confirmation text immediately after booking and a reminder the morning of their appointment.
- **Handles after-hours** — detects business hours (Mon–Fri 8AM–6PM) and switches to a closed greeting automatically.
- **Lives in your knowledge base** — answers questions about services, pricing, service area, and policies using your own documents.

---

## Architecture

```
Caller
  ↓
Twilio (inbound call + SMS)
  ↓
Deepgram nova-2 (speech-to-text, ~280ms)
  ↓
FastAPI Backend
  ├── Qdrant (RAG — company knowledge documents)
  └── Claude Sonnet (LLM reasoning + tool use, streaming)
  ↓
ElevenLabs (text-to-speech) → Twilio (audio playback → caller)
  ↓
PostgreSQL (call logs, transcripts, appointments, customers)
  ↓
HubSpot / Jobber / Housecall Pro / QuickBooks / Google Calendar
  ↓
SMS confirmation → caller + morning reminder (APScheduler 8 AM)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| LLM | Claude Sonnet (Anthropic) |
| Embeddings | Voyage AI (voyage-3, 1024 dims) |
| Vector DB | Qdrant |
| Relational DB | PostgreSQL (Supabase) |
| Voice | Twilio Voice API |
| Speech-to-Text | Deepgram nova-2 |
| Text-to-Speech | ElevenLabs |
| CRM | HubSpot API |
| Field Service | Jobber, Housecall Pro, QuickBooks |
| Scheduling | Google Calendar API (service account) |
| SMS | Twilio Messaging |
| Job Scheduler | APScheduler |
| Infrastructure | Docker, Docker Compose, AWS EC2 |

---

## Features

### Voice Pipeline
- Inbound calls via Twilio webhook
- Deepgram nova-2 transcription — optimised for phone audio, handles accents and noise
- Claude streams the first sentence while generating the rest — caller hears a response in under 1 second
- ElevenLabs text-to-speech played back via Twilio

### RAG Knowledge System
- Upload plain text or markdown documents via the dashboard
- Automatically chunks, embeds, and indexes in Qdrant
- Semantic search retrieves relevant context on every call
- Claude answers are grounded in real business data — no hallucination

### Appointment Booking
- Checks live availability from Google Calendar
- Presents open slots and confirms with the caller
- Conflict detection prevents double-booking
- Claude uses structured tool calls (`check_availability` + `book_appointment`)
- Asks diagnostic questions and confirms caller name spelling before booking

### CRM & Integrations
- HubSpot: creates or updates contact + deal on every completed call
- Jobber: creates job ticket with caller details and appointment
- Housecall Pro: creates customer + job
- QuickBooks: creates customer record
- Integration API keys stored per business in the config panel; all integrations fire in parallel after call ends

### Post-Call Automation
- SMS confirmation sent to caller immediately after booking
- Morning-of reminder SMS via APScheduler at 8 AM (America/Chicago)
- Email summary sent to business owner via Gmail SMTP

### Customer Recognition
- Callers identified by phone number on inbound
- Returning customers greeted by name
- Full call history injected into conversation context

### After-Hours Handling
- Current Austin time injected into system prompt on every call
- Closed greeting if call arrives outside Mon–Fri 8AM–6PM

### Admin Dashboard
- View every call with transcript, AI summary, and booking status
- Call volume by day (14-day), peak hours, and service breakdown analytics (Chart.js)
- Manage knowledge base documents (upload, preview, delete)
- Configure business settings, services, and integration API keys
- Dashboard protected by password-based session authentication

---

## Project Structure

```
cleo/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── call.py              # Twilio webhooks — incoming, /call/response, /call/continue, status
│   │   │   ├── stream.py            # Deepgram WebSocket — STT + kicks off Claude in background
│   │   │   ├── conversation.py      # Conversation endpoint
│   │   │   ├── documents.py         # RAG document management
│   │   │   ├── appointments.py      # Booking endpoints
│   │   │   ├── customers.py         # Customer management
│   │   │   ├── calls.py             # Call history
│   │   │   ├── analytics.py         # Call volume, peak hours, service breakdown
│   │   │   ├── business.py          # Business config CRUD
│   │   │   ├── auth.py              # Dashboard session auth
│   │   │   └── health.py
│   │   ├── services/
│   │   │   ├── conversation_service.py    # Claude tool use, streaming, session history, system prompt
│   │   │   ├── calendar_service.py        # Google Calendar free/busy + event creation
│   │   │   ├── sms_service.py             # Twilio SMS — confirmation + morning reminders
│   │   │   ├── email_service.py           # Gmail SMTP post-call summary
│   │   │   ├── business_service.py        # Business config singleton with 60s cache
│   │   │   ├── integration_service.py     # Extracts structured call data with Claude, fans out to integrations
│   │   │   ├── integrations/
│   │   │   │   ├── hubspot.py
│   │   │   │   ├── jobber.py
│   │   │   │   ├── housecall_pro.py
│   │   │   │   └── quickbooks.py
│   │   │   ├── document_service.py
│   │   │   ├── appointment_service.py
│   │   │   ├── customer_service.py
│   │   │   ├── call_service.py
│   │   │   ├── tts_service.py
│   │   │   └── stt_service.py
│   │   ├── models/
│   │   │   ├── business.py
│   │   │   ├── call.py
│   │   │   ├── appointment.py
│   │   │   ├── customer.py
│   │   │   └── document.py
│   │   ├── core/
│   │   │   ├── state.py             # In-memory call state (pending_first, pending_rest, call_phone_map, etc.)
│   │   │   ├── database.py
│   │   │   ├── qdrant.py
│   │   │   └── config.py
│   │   └── main.py                  # APScheduler 8AM reminders, dashboard auth middleware, static mount
│   ├── static/                      # Dashboard frontend (HTML/Tailwind/Chart.js)
│   │   ├── index.html               # Analytics
│   │   ├── calls.html               # Call list + transcript viewer
│   │   └── config.html              # Business settings
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml               # Local development
├── docker-compose.prod.yml          # Production (AWS EC2)
├── .env.example
└── apex_home_services.txt
```

---

## Getting Started

### Prerequisites
- Docker Desktop
- ngrok (for local Twilio webhook tunneling)
- Accounts: Twilio, Deepgram, Anthropic, Voyage AI, ElevenLabs
- Optional: HubSpot, Jobber, Housecall Pro, QuickBooks, Google Calendar API credentials

### 1. Clone and configure

```bash
git clone https://github.com/JahanzebKayanii/Cleo.ai
cd cleo
cp .env.example .env
```

Fill in your API keys in `.env`.

### 2. Start the stack

```bash
docker compose up --build
```

Starts PostgreSQL, Qdrant, and the FastAPI backend. Tables and collections are created on first run.

### 3. Upload a knowledge document

```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@apex_home_services.txt"
```

Or use the dashboard at `http://localhost:8000/dashboard/`.

### 4. Expose your local server

```bash
ngrok http 8000
```

### 5. Configure Twilio

In your Twilio phone number settings:
- **Voice webhook:** `https://<ngrok-url>/call/incoming` (HTTP POST)
- **Status callback:** `https://<ngrok-url>/call/status` (HTTP POST)

### 6. Call your Twilio number

Cleo answers, transcribes with Deepgram, searches the knowledge base, and responds via Claude.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | System health check |
| POST | `/auth/login` | Dashboard login |
| POST | `/auth/logout` | Dashboard logout |
| POST | `/documents/upload` | Upload a knowledge document |
| GET | `/documents/` | List all documents |
| DELETE | `/documents/{id}` | Delete a document |
| GET | `/documents/search?q=` | Semantic search |
| POST | `/call/incoming` | Twilio inbound call webhook |
| POST | `/call/response` | Claude response (first turn) |
| POST | `/call/continue` | Claude response (subsequent turns) |
| POST | `/call/status` | Twilio call status callback |
| GET | `/calls/` | List all calls |
| GET | `/calls/{id}` | Get call with transcript |
| GET | `/analytics/overview` | Call volume, peak hours, service breakdown |
| GET | `/business/config` | Get business configuration |
| PUT | `/business/config` | Update business configuration |
| POST | `/business/test-integrations` | Test CRM integration connections |
| POST | `/appointments/create` | Book an appointment |
| GET | `/appointments/slots?date=` | Get available slots |
| POST | `/customers/` | Create or find customer |
| GET | `/customers/{id}` | Get customer by ID |

---

## Environment Variables

```env
# Database (use DATABASE_URL for Supabase, or individual vars for local Docker)
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
# POSTGRES_USER=cleo
# POSTGRES_PASSWORD=cleo_pass
# POSTGRES_DB=cleo_db

# Qdrant (use QDRANT_URL + QDRANT_API_KEY for cloud, or host/port for local)
QDRANT_URL=https://[cluster-id].us-east4-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=...
QDRANT_COLLECTION=cleo_docs

# AI
ANTHROPIC_API_KEY=sk-ant-...
VOYAGE_API_KEY=pa-...

# Voice
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...
DEEPGRAM_API_KEY=...

# Text-to-Speech
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...

# Google Calendar (service account key, base64-encoded)
GOOGLE_CALENDAR_ID=...
GOOGLE_SERVICE_ACCOUNT_B64=...

# Email (Gmail SMTP)
GMAIL_USER=your@gmail.com
GMAIL_APP_PASSWORD=...

# Jobber OAuth (optional)
JOBBER_CLIENT_ID=...
JOBBER_CLIENT_SECRET=...

# App
APP_ENV=production
BASE_URL=https://your-ec2-ip-or-domain.com
DASHBOARD_PASSWORD=your_password
```

---

## Roadmap

- [ ] Live Transfer — Cleo transfers frustrated callers to a human
- [ ] Web Chat Widget — Cleo embedded on website as chatbox
- [ ] Email Follow-up — call summary sent to the customer after the call
- [ ] Call Recording Playback — play back Twilio recordings from dashboard
- [ ] A2P 10DLC registration — unblocks SMS confirmations (Twilio console only, no code changes needed)
- [ ] ServiceTitan — apply for partner access once traction
- [ ] Multi-tenant — support multiple business clients
