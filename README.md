# ElevenLabs-X-MCP

### Assumptions
- Timezone is IST (not handling locale)
- Spoken language is English

### Google Calendar API
 - https://developers.google.com/workspace/calendar/api/v3/reference/freebusy
 - https://developers.google.com/workspace/calendar/api/v3/reference/events/quickAdd (uses LLM's maybe, no cost)


### Attempted Solutions:

- Zapier MCP (easy, quick, predefined tools)
- Custom MCP (hosted locally via Ngrok)

## Local MCP
To generate a bearer token for server auth
```bash
uv run authentication/generate_key.py
```
Use this key while setting up ElevenLabs MCP Integration

```bash
uv run src/server.py
```

```bash
ngrok http http://127.0.0.1:8000
```

