# AI Scheduling Assistant

A production-grade AI scheduling assistant that manages Google Calendar through natural language conversations via SMS/WhatsApp. Built with OpenAI's GPT-4 and Twilio.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📅 **Natural Language Scheduling** - "Schedule a meeting tomorrow at 3pm for 90 minutes"
- 🔍 **Smart Event Resolution** - "Move my 3pm to Friday" automatically finds the right event
- ✅ **Two-Phase Confirmation** - Moves and deletes require explicit "yes" confirmation
- 🕐 **Flexible Time Parsing** - Understands "in 2 hours", "next Friday", "end of day", etc.
- 💬 **Conversational UI** - Feels like texting a real assistant, not a robot
- 🔒 **Anti-Hallucination Guards** - Prevents the AI from claiming actions it didn't take
- 📱 **Channel Agnostic** - Designed to support SMS, WhatsApp, and voice (coming soon)

## Demo Conversation

```
You: "What's on my calendar tomorrow?"
Assistant: "Here's your schedule for Friday, Feb 7:
  - 9:00 AM - 10:00 AM: Team Standup
  - 2:00 PM - 3:30 PM: Client Call
  - 4:00 PM - 5:00 PM: Project Review"

You: "Move the client call to 3pm"
Assistant: "Just to confirm - move **Client Call** from Fri Feb 7, 2:00 PM - 3:30 PM 
to Fri Feb 7, 3:00 PM - 4:30 PM?

Reply **yes** to confirm or **no** to cancel."

You: "yes"
Assistant: "Done! I've moved **Client Call** to Fri Feb 7, 3:00 PM - 4:30 PM."
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CHANNEL ADAPTERS                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Twilio    │  │   Twilio    │  │   Future    │             │
│  │  SMS/WA     │  │   Voice     │  │  Channels   │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
└─────────┼────────────────┼────────────────┼─────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CONVERSATION ENGINE                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              ConversationState (per user)                │   │
│  │  - messages[]     - pending_action    - event_registry  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│  ┌───────────────────────────▼───────────────────────────────┐ │
│  │                   AssistantEngine                         │ │
│  │  - process_message()  - tool execution  - confirmations   │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                      TOOL LAYER                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐   │
│  │  Calendar  │  │   Time     │  │   Event Reference      │   │
│  │   Tools    │  │   Tools    │  │   Registry (anti-hall.)│   │
│  └────────────┘  └────────────┘  └────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Python 3.10+
- Google Cloud account with Calendar API enabled
- OpenAI API key
- Twilio account (for SMS/WhatsApp)
- ngrok or similar (for local development)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-scheduling-assistant.git
cd ai-scheduling-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **Google Calendar API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client IDs**
5. Select "Desktop application"
6. Download the credentials JSON file
7. Rename it to `credentials.json` and place in project root
8. Run the auth script:

```bash
python scripts/setup_google_auth.py
```

This will open a browser for authentication and create `token.json`.

### 5. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o
OWNER_NAME=YourName
```

### 6. Set Up Twilio

1. Get your Twilio Account SID and Auth Token from [Twilio Console](https://console.twilio.com/)
2. Get a Twilio phone number with SMS capability
3. For WhatsApp, set up the [Twilio Sandbox for WhatsApp](https://www.twilio.com/docs/whatsapp/sandbox)

### 7. Run the Server

```bash
python app.py
```

### 8. Expose Local Server (for development)

```bash
ngrok http 5000
```

### 9. Configure Twilio Webhook

In your Twilio Console, set the webhook URL for your phone number:
- **SMS**: `https://your-ngrok-url.ngrok.io/sms`
- **WhatsApp**: Same URL for your WhatsApp sandbox

## Project Structure

```
ai-scheduling-assistant/
├── app.py                    # Flask application (thin routing layer)
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
│
├── engine/                  # Core conversation engine
│   ├── __init__.py
│   ├── assistant.py         # Main orchestration & tool execution
│   ├── conversation.py      # State management per user
│   └── prompts.py           # System prompts for the AI
│
├── tools/                   # Calendar and time tools
│   ├── __init__.py
│   ├── calendar_ops.py      # Google Calendar API operations
│   ├── time_ops.py          # Natural language time parsing
│   ├── event_refs.py        # Event reference registry (anti-hallucination)
│   └── registry.py          # OpenAI function/tool definitions
│
├── adapters/                # Channel adapters (SMS, Voice, etc.)
│   ├── __init__.py
│   ├── base.py              # Abstract adapter interface
│   └── twilio_sms.py        # Twilio SMS/WhatsApp adapter
│
├── utils/                   # Utilities
│   ├── __init__.py
│   ├── errors.py            # Custom exceptions
│   └── logging.py           # Structured logging
│
└── scripts/                 # Setup scripts
    └── setup_google_auth.py # Google OAuth setup
```

## Configuration

All configuration is managed through environment variables and `config.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | Model to use | `gpt-4o` |
| `OWNER_NAME` | Name the assistant uses | `Brandon` |

## Key Design Decisions

### Two-Phase Confirmation
All destructive operations (move, delete) require explicit confirmation:
1. User requests action → Assistant stages it and asks for confirmation
2. User confirms with "yes" → Action is executed

### Event Reference Registry
Instead of exposing raw Google Calendar event IDs to the AI, we use opaque tokens (`evt_1`, `evt_2`). This prevents:
- AI hallucinating plausible-looking event IDs
- Stale references from old conversations
- Security issues from exposed internal IDs

### Hallucination Detection
The system actively checks if the AI claims to have performed an action without actually calling the appropriate tools, and corrects course if detected.

### Channel-Agnostic Design
The `AssistantEngine` is completely decoupled from Twilio. Adding new channels (Slack, Discord, Voice) only requires implementing a new adapter.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sms` | POST | Twilio SMS/WhatsApp webhook |
| `/voice` | POST | Twilio Voice webhook (placeholder) |
| `/health` | GET | Health check |

## Extending the Assistant

### Adding New Tools

1. Add the tool definition in `tools/registry.py`
2. Implement the tool logic in `engine/assistant.py` under `_execute_tool()`
3. Update the system prompt in `engine/prompts.py` if needed

### Adding New Channels

1. Create a new adapter in `adapters/` implementing `ChannelAdapter`
2. Add a new route in `app.py` that uses your adapter
3. The `AssistantEngine.process_message()` works the same regardless of channel

## Production Deployment

### Recommended Setup

- **Hosting**: Railway, Render, AWS, or any Python-compatible host
- **State Storage**: Replace in-memory stores with Redis
- **Logging**: Ship logs to CloudWatch, Datadog, or similar
- **Monitoring**: Add Sentry for error tracking

### Environment Variables for Production

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
OWNER_NAME=YourName
FLASK_ENV=production
```

### Security Checklist

- [ ] Validate Twilio webhook signatures
- [ ] Use HTTPS only
- [ ] Keep `token.json` and `.env` out of version control
- [ ] Set up rate limiting
- [ ] Monitor for abuse

## Troubleshooting

### "Event not found" errors
The event may have been deleted or the reference expired. Ask the assistant to show your schedule first.

### Assistant claims to delete but nothing happens
Check the logs for hallucination detection. The updated code should catch this and ask for clarification.

### Time parsing issues
The assistant understands most natural language times. If something doesn't work, try being more explicit: "tomorrow at 3:00 PM" instead of "tomorrow afternoon".

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with [OpenAI GPT-4](https://openai.com/)
- SMS/WhatsApp integration via [Twilio](https://www.twilio.com/)
- Calendar integration via [Google Calendar API](https://developers.google.com/calendar)
