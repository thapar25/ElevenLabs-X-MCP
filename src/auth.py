from fastmcp.server.auth import BearerAuthProvider
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_credentials() -> Credentials:
    """
    Obtain and refresh Google Calendar API credentials.

    Returns:
        Credentials: The valid credentials object.
    """
    creds = None

    token_path = "authentication/token.json"
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds


public_key_path = "authentication/public.pem"
if not os.path.exists(public_key_path):
    raise FileNotFoundError(
        f"Public key file not found at {public_key_path}. Please ensure it is present."
    )

with open(public_key_path, "r") as f:
    public_key_pem = f.read().encode("utf-8")

auth_provider = BearerAuthProvider(
    public_key=public_key_pem,
    issuer=os.getenv("AUTH_ISSUER"),
    audience=os.getenv("AUTH_AUDIENCE"),
    algorithm="RS256",
)
