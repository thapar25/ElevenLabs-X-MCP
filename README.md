# ElevenLabs-X-MCP

A voice-driven calendar management system that integrates ElevenLabs' speech synthesis with Google Calendar via Model Context Protocol (MCP). Schedule, modify, and query your calendar using natural voice commands.


## 🎯 Features

- **Voice-Activated Calendar Management**: Schedule meetings, check availability, and modify events through natural speech
- **Real-time Calendar Integration**: Direct Google Calendar API access for seamless synchronization
- **Intelligent Time Parsing**: Handles relative time references and complex scheduling logic
- **Multi-deployment Options**: Use the live server or deploy locally
- **IST Timezone Optimized**: Built specifically for Indian Standard Time

## 🏗️ Architecture

- **Live Server**: Hosted on Render.com for immediate use
- **Local Development**: Self-hosted option with ngrok tunneling
- **Authentication**: Bearer token-based security
- **API Integration**: Google Calendar API v3 with free/busy and quick-add functionality

###  Tool Test (Claude Sonnet 4) ✅
[Conversation Link](https://claude.ai/share/7ee8b2b1-8c8e-404f-a0f3-369317be833d) ⭐⭐⭐⭐



### Assumptions
- Timezone is IST (not handling locale)
- Spoken language is English

### Google Calendar API

- [Get Free/Busy slots](https://developers.google.com/workspace/calendar/api/v3/reference/freebusy)
- [Quick Add Events](https://developers.google.com/workspace/calendar/api/v3/reference/events/quickAdd) (uses LLM's maybe, no cost)


### Attempted Solutions:

- Zapier MCP (easy, quick, predefined tools)
- Custom MCP (hosted locally via [Ngrok](http://ngrok.com/))
- Custom MCP (hosted on [Render.com](https://render.com/)) [[Currently Live](https://elevenlabs-x-mcp.onrender.com/health)]



# 🚀 Quick Start
## Option 1: Use Live Server (Recommended)

1. Get Your Bearer Token

- Clone this repository
- Navigate to authentication/ directory
- Run the token generation notebook (see Token Generation)


2. Configure ElevenLabs MCP Integration

- Use the live server endpoint: https://your-render-app.onrender.com/mcp
- Enter your generated bearer token



[Screenshot placeholder: ElevenLabs MCP configuration interface]
## Option 2: Local Development

1. Clone and Setup
```bash
git clone https://github.com/thapar25/ElevenLabs-X-MCP.git
cd ElevenLabs-X-MCP
uv sync
```

2. Generate Authentication Token
```bash
uv run authentication/generate_key.py
```

Start Local Server
```bash
uv run src/server.py
```

Expose via ngrok
```bash
ngrok http http://127.0.0.1:8000
```
## 🔐 Token Generation

The project includes Jupyter notebooks for secure token generation and Google Calendar authentication.

### Authentication Flow

1. **Google Calendar Setup**
   - Navigate to `authentication/google_calendar_setup.ipynb`
   - Follow the OAuth2 flow to authorize calendar access
   - Generate and store your credentials securely

[Screenshot placeholder: Google OAuth consent screen]

2. **Bearer Token Generation**
   - Open `authentication/token_generator.ipynb`
   - Run all cells to generate your unique bearer token
   - This token authenticates your requests to the MCP server

[Screenshot placeholder: Jupyter notebook showing successful token generation]

### Token Security Notes

- Tokens are generated locally and never transmitted during creation
- Store your bearer token securely - it provides full calendar access
- Regenerate tokens periodically for enhanced security

[Screenshot placeholder: Terminal showing server startup and ngrok URL]


## 🌐 Deployment

### Render.com (Production)

The live server is deployed on Render.com with:
- Automatic deployments from main branch
- Environment variable management for secrets
- Built-in SSL and custom domain support

[Screenshot placeholder: Render deployment dashboard]

### Local Development with ngrok

For development and testing:
1. Start the local server on port 8000
2. Use ngrok to create a public tunnel
3. Configure ElevenLabs with the ngrok URL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test with both local and live server configurations
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Security Considerations

- Never commit bearer tokens or Google credentials to version control
- Use environment variables for production deployments
- Regularly rotate authentication tokens
- Monitor API usage for unusual activity

---





