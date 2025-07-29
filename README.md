# ElevenLabs-X-MCP

A voice-driven calendar management system that integrates ElevenLabs' speech synthesis with Google Calendar via Model Context Protocol (MCP). Schedule, modify, and query your calendar using natural voice commands.

## Demo
[Demo Video](https://www.loom.com/share/2c68ea3497da4a849a62c76d6dfd3a72?sid=188ddcac-55fe-4a81-9885-4fd5be4f79e7)

## Evaluation by ChatGPT

This evaluation reviews a scheduling chatbot's performance during a multi-turn scheduling conversation. The bot handled everything from simple booking to conflict resolution and last-minute pivots—without access to search functionality (e.g., it could not search for event titles, only list events based on time).

---

### 📊 Final Score: **90 / 100**  
**Grade:** A−

---

### 🧪 Scoring Breakdown

| **Category**                   | **Max Points** | **Score** | **Notes**                                                                 |
|-------------------------------|----------------|-----------|---------------------------------------------------------------------------|
| ✅ Basic Functionality         | 20             | 20        | Seamless handling of standard scheduling flows                           |
| 🧠 Time Parsing                | 20             | 18        | Understood vague phrases like "late next week" and "before my flight"    |
| 🔄 Context & Conflict Handling | 20             | 18        | Adapted to mid-convo changes and complex rescheduling                    |
| ⚠️ Edge Case Detection         | 20             | 17        | Flagged 25-hour session; minor issue with post-Christmas date logic      |
| 🔍 Proactive Guidance          | 20             | 17        | Could be more assertive suggesting alternate slots when schedules are tight |

---

### ⚠️ Limitations Considered

- **No Search Functionality**: The bot was **not capable of finding events by title**, only by time blocks.  
  ➤ This explains why it didn’t respond to “after the Project Alpha kickoff” with context—**not a flaw**, just a constraint.

---

### 💡 Opportunities for Improvement

- Improve **calendar awareness** (e.g., business day logic around holidays).
- Offer **broader time slot suggestions** proactively when conflicts arise.
- Add **search functionality for event names** in future iterations to enhance context handling.

---

### 🏁 Conclusion

A strong A− performance. This chatbot was resilient, accurate, and maintained flow despite shifting user intent. With minor improvements in calendar logic and proactive assistance, it could easily hit A+ territory.


[Evaluation conversation](https://chatgpt.com/share/6887a046-6cf0-8011-81e7-edb21f25b0d1)

## Preparing the demo (using GenAI)
The MCP server can be run locally on Claude Desktop to generate mock scenarios to test the agent. [Conversation Link](https://claude.ai/share/10cdb489-ec34-4088-a069-f22f1c709ddd)

*Sample claude_desktop_config.json:*
```
{
  "mcpServers": {
    "calendar": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\Users\\Thapar\\Documents\\VSCode Files\\ElevenLabs-X-MCP",
        "C:\\Users\\Thapar\\Documents\\VSCode Files\\ElevenLabs-X-MCP\\.venv\\Scripts\\python.exe",
        "src/server.py",
        "--transport",
        "stdio"
      ]
    }
  }
}
```


## 🎯 Features

- **Voice-Activated Calendar Management**: Schedule meetings, check availability, and modify events through natural speech
- **Real-time Calendar Integration**: Direct Google Calendar API access for seamless synchronization
- **Intelligent Time Parsing**: Handles relative time references and complex scheduling logic
- **Multi-deployment Options**: Use the live server or deploy locally
- **IST Timezone Optimized**: Built specifically for Indian Standard Time

## 🏗️ Architecture

- **Remote MCP Server**: Hosted on Render.com for immediate use
- **ElevenLabs Conversational Agents**: Utilizes GenAI agents with voice capabilities to enhance user interaction
- **Authentication**: Implements Bearer token-based security for secure access control
- **API Integration**: Integrates Google Calendar API v3, supporting free/busy checks and quick-add functionality for efficient scheduling

###  Tool Test (Claude Sonnet 4) ✅
[Conversation Link](https://claude.ai/share/7ee8b2b1-8c8e-404f-a0f3-369317be833d) ⭐⭐⭐⭐


### Assumptions
- **Timezone**: The application assumes IST (Indian Standard Time) and does not handle other locales.
- **Language**: English is the spoken language assumed for voice commands.

### Google Calendar API

- [Get Free/Busy slots](https://developers.google.com/workspace/calendar/api/v3/reference/freebusy)
- [Quick Add Events](https://developers.google.com/workspace/calendar/api/v3/reference/events/quickAdd) (uses LLM's maybe, no cost)


### Attempted Solutions:

- Zapier MCP (easy, quick, predefined tools)
- Custom MCP (hosted locally via [Ngrok](http://ngrok.com/))
- Custom MCP (hosted on [Render.com](https://render.com/)) [[Currently Live](https://elevenlabs-x-mcp.onrender.com/health)]


## 🔐 Token Generation

The project includes Jupyter notebooks for secure token generation and Google Calendar authentication.

1. **Google Calendar Setup**
   - Navigate to `notebooks/generate_token.ipynb`
   - Follow the [OAuth2 flow](https://developers.google.com/identity/protocols/oauth2/web-server) to authorize calendar access
   - Generate and store your credentials securely (json)
   <img width="1021" height="97" alt="image" src="https://github.com/user-attachments/assets/19ddeabb-9b4f-4627-ad97-861b04d4d330" />

2. **Bearer Token Generation**
   - When the MCP server is deployed, a test token is printed in the console.
   - Copy the token and use it as a secret on ElevenLabs Conversational Platform
<img width="1611" height="868" alt="image" src="https://github.com/user-attachments/assets/31668868-cf9d-40e0-8b0d-2071351fcf5a" />


# 🚀 Quick Start
## Option 1: Host MCP Server on Render.com

1. Get Your ENV VARS

Ensure the following environment variables are configured at the time of deployment to Render:

- `AUTH_ISSUER`: Set this to `"https://dev.example.com"`.
- `AUTH_AUDIENCE`: Set this to `"my-dev-server"`.
- `GOOGLE_CREDS_BASE64`: Obtain this string by running the `generate_token.ipynb` Jupyter Notebook.

[Reference](https://render.com/docs/docker#building-from-a-dockerfile)

2. Configure ElevenLabs MCP Integration

- Enter your generated bearer token as secret
  
<img width="510" height="191" alt="image" src="https://github.com/user-attachments/assets/06d21e1b-49e0-48a4-af4e-791108c157e6" />

  
- Use the live server endpoint: https://your-render-app.onrender.com/mcp

<img width="525" height="287" alt="image" src="https://github.com/user-attachments/assets/b327f0df-98d1-4713-af1a-34d9b82ba512" />


## Option 2: Local Development (and remote access using Ngrok)

1. Clone and Setup
```bash
git clone https://github.com/thapar25/ElevenLabs-X-MCP.git
cd ElevenLabs-X-MCP
uv sync
```
2. Generate [`credentials.json`](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred) file from Google Console and place the file in root directory.

3. Run `notebooks\generate_token.ipynb` to get GOOGLE_CREDS_BASE64. 

4. Generate Authentication Token
```bash
uv run authentication/generate_key.py
```

4. Start Local Server
```bash
uv run src/server.py
```

5. Expose via ngrok
```bash
ngrok http http://127.0.0.1:8000
```


### Token Security Notes

- Tokens are generated locally and never transmitted during creation
- Store your bearer token securely - it provides full calendar access
- Regenerate tokens periodically for enhanced security


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


## ⚠️ Security Considerations

- Never commit bearer tokens or Google credentials to version control
- Use environment variables for production deployments
- Regularly rotate authentication tokens
- Monitor API usage for unusual activity

---





