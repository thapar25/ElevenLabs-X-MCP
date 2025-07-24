from fastmcp.server.auth import BearerAuthProvider
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = "authentication/credentials.json"

            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"Credentials file not found at {credentials_path}. Please ensure it is present."
                )

            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())

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
