# Detailed Setup Guide

This guide walks you through setting up the AI Scheduling Assistant from scratch.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Google Calendar API Setup](#google-calendar-api-setup)
3. [OpenAI API Setup](#openai-api-setup)
4. [Twilio Setup](#twilio-setup)
5. [Local Development](#local-development)
6. [Testing](#testing)
7. [Production Deployment](#production-deployment)

---

## Prerequisites

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **A Google account** - For Google Calendar access
- **ngrok** (for local development) - [Download ngrok](https://ngrok.com/download)

---

## Google Calendar API Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top → **New Project**
3. Name it something like "AI Scheduling Assistant"
4. Click **Create**

### Step 2: Enable the Google Calendar API

1. In your project, go to **APIs & Services** → **Library**
2. Search for "Google Calendar API"
3. Click on it and press **Enable**

### Step 3: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth 2.0 Client IDs**
3. If prompted, configure the OAuth consent screen:
   - User Type: **External** (or Internal if using Google Workspace)
   - App name: "AI Scheduling Assistant"
   - User support email: Your email
   - Developer contact: Your email
   - Click **Save and Continue** through the scopes (no changes needed)
   - Add yourself as a test user
   - Click **Save and Continue**
4. Back in Credentials, create OAuth 2.0 Client ID:
   - Application type: **Desktop app**
   - Name: "AI Scheduling Assistant"
   - Click **Create**
5. Click **Download JSON** on the created credential
6. Rename the downloaded file to `credentials.json`
7. Move it to your project root directory

### Step 4: Authorize the Application

```bash
python scripts/setup_google_auth.py
```

This will:
1. Open a browser window
2. Ask you to sign in to Google
3. Request permission to access your calendar
4. Create a `token.json` file with your credentials

---

## OpenAI API Setup

### Step 1: Get an API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to **API Keys** → **Create new secret key**
4. Copy the key (you won't be able to see it again!)

### Step 2: Configure the Environment

Add to your `.env` file:
```
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
```

**Note on Models:**
- `gpt-4o` - Best quality, recommended
- `gpt-4-turbo` - Good balance of quality and cost
- `gpt-3.5-turbo` - Cheapest, but may have quality issues with complex scheduling

---

## Twilio Setup

### Step 1: Create a Twilio Account

1. Go to [Twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free account
3. Verify your phone number

### Step 2: Get a Phone Number

1. In Twilio Console, go to **Phone Numbers** → **Buy a number**
2. Choose a number with SMS capability
3. Note down your:
   - Account SID (from Dashboard)
   - Auth Token (from Dashboard)
   - Phone Number

### Step 3: For WhatsApp (Optional)

1. Go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Follow the sandbox setup instructions
3. Send the join code from your WhatsApp to the Twilio sandbox number

### Step 4: Configure Webhook

After starting your server and ngrok:

1. Go to **Phone Numbers** → **Manage** → **Active Numbers**
2. Click on your number
3. Under "Messaging", set:
   - **When a message comes in**: `https://your-ngrok-url.ngrok.io/sms`
   - Method: HTTP POST

For WhatsApp sandbox:
1. Go to **Messaging** → **Settings** → **WhatsApp sandbox settings**
2. Set the webhook URL to the same `/sms` endpoint

---

## Local Development

### Step 1: Clone and Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-scheduling-assistant.git
cd ai-scheduling-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your values
```

### Step 2: Run the Server

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 3: Expose with ngrok

In a new terminal:
```bash
ngrok http 5000
```

Copy the `https://xxxxx.ngrok.io` URL and configure it in Twilio.

### Step 4: Test

Send a text message to your Twilio number:
```
What's on my calendar today?
```

---

## Testing

### Manual Testing Checklist

1. **View Schedule**
   - Send: "What's on my calendar today?"
   - Should return your events or say the calendar is clear

2. **Create Event**
   - Send: "Schedule a test meeting tomorrow at 2pm"
   - Should confirm the event was created
   - Check your Google Calendar to verify

3. **Move Event (with confirmation)**
   - Send: "Move the test meeting to 3pm"
   - Should ask for confirmation
   - Reply: "yes"
   - Check your Google Calendar to verify

4. **Delete Event (with confirmation)**
   - Send: "Delete the test meeting"
   - Should ask for confirmation
   - Reply: "yes"
   - Check your Google Calendar to verify

### Checking Logs

The server outputs JSON logs. Look for:
- `"message": "Executing tool: ..."` - Tools being called
- `"message": "Handling confirmation"` - Confirmation flow
- `"message": "Executing DELETE"` - Actual deletions

---

## Production Deployment

### Option 1: Railway

1. Push your code to GitHub
2. Go to [Railway](https://railway.app/)
3. New Project → Deploy from GitHub repo
4. Add environment variables in Railway dashboard
5. Railway will auto-deploy and give you a URL

### Option 2: Render

1. Push your code to GitHub
2. Go to [Render](https://render.com/)
3. New Web Service → Connect your repo
4. Add environment variables
5. Deploy

### Option 3: AWS / GCP / Azure

For more control, deploy to a cloud VM:
1. Set up a server with Python
2. Use gunicorn as the WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. Set up nginx as a reverse proxy
4. Use systemd to keep the service running

### Production Checklist

- [ ] Use HTTPS (required for Twilio webhooks)
- [ ] Validate Twilio webhook signatures
- [ ] Set up proper logging (CloudWatch, Datadog, etc.)
- [ ] Monitor error rates
- [ ] Set up alerts for failures
- [ ] Consider rate limiting
- [ ] Back up your `token.json` securely

---

## Troubleshooting

### "Invalid grant" error with Google
Your `token.json` may be expired. Delete it and run `setup_google_auth.py` again.

### Twilio not receiving messages
- Check webhook URL is correct
- Ensure ngrok is running (for local dev)
- Check Twilio error logs in the console

### Assistant not responding
- Check Flask logs for errors
- Verify OPENAI_API_KEY is set correctly
- Check OpenAI API status page

### Events not being modified
- Check logs for "Executing tool" messages
- Make sure you're confirming with "yes"
- Look for hallucination detection warnings in logs
