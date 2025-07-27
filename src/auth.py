from fastmcp.server.auth import BearerAuthProvider
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_credentials() -> Credentials:
    """
    Obtain and refresh Google Calendar API credentials.

    Returns:
        Credentials: The valid credentials object.
    """
    creds = None
    credentials_path = "authentication/service_account.json"
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Service account file not found at {credentials_path}. Please ensure it is present."
        )
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )

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
