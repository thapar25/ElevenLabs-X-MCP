# ElevenLabs-X-MCP

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

