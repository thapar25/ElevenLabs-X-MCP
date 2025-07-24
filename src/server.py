import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastmcp import FastMCP
from utils import to_rfc3339, format_dt
from fastmcp.server.middleware import Middleware, MiddlewareContext
import os
from dotenv import load_dotenv
from starlette.responses import JSONResponse

_ = load_dotenv()


mcp = FastMCP(name="Google Calendar", debug=True)


class AuthMiddleware(Middleware):
    """Middleware that checks for Bearer token authentication."""

    async def on_message(self, context: MiddlewareContext, call_next):
        auth_header = context.fastmcp_context.get_http_request().headers.get(
            "Authorization"
        )
        secret = os.environ.get("SECRET")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Missing or invalid Authorization header"}, 401
        token = auth_header.split("Bearer ")[-1]
        if token != secret:
            return {"error": "Invalid token"}, 403
        return await call_next(context)


mcp.add_middleware(AuthMiddleware())


SCOPES = ["https://www.googleapis.com/auth/calendar"]


@mcp.tool()
def get_events_today() -> str:
    """
    Get today's events from the user's Google Calendar.

    Returns:
        str: A formatted string of today's events.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now_utc = datetime.datetime.now(tz=datetime.timezone.utc)
        ist_offset = datetime.timedelta(hours=5, minutes=30)
        ist = datetime.timezone(ist_offset)
        now_ist = now_utc.astimezone(ist)
        today_ist = now_ist.date()
        end_of_day_ist = datetime.datetime.combine(
            today_ist,
            datetime.time(
                hour=23, minute=59, second=59, microsecond=999999, tzinfo=ist
            ),
        )
        now_iso = now_ist.isoformat()
        end_of_day_iso = end_of_day_ist.isoformat()
        print("Getting the upcoming events for today...")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now_iso,
                timeMax=end_of_day_iso,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            return "No upcoming events found."

        response = []
        for event in events:
            start_time = event["start"].get("dateTime", event["start"].get("date"))
            end_time = event["end"].get("dateTime", event["end"].get("date"))
            title = event.get("summary", "Untitled Event")
            location = event.get("location", "No Location specified")
            description = event.get("description", "No Description provided")
            hangout_link = event.get("hangoutLink", "No meeting link provided")
            start = format_dt(start_time)
            end = format_dt(end_time)
            response.append(
                f"Event: {title}\nDescription: {description}\nStart: {start}\nEnd: {end}\nLocation: {location}\nMeeting Link: {hangout_link}\n"
            )
        return "\n".join(response)

    except HttpError as error:
        return f"An error occurred: {error}"


@mcp.tool()
def get_busy_slots(start_time: str, end_time: str) -> str:
    """
    Get busy slots in the user's Google Calendar between start_time and end_time.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        busy_slots = (
            service.freebusy()
            .query(
                body={
                    "timeMin": to_rfc3339(start_time),
                    "timeMax": to_rfc3339(end_time),
                    "timeZone": "IST",
                    "items": [{"id": "primary"}],
                }
            )
            .execute()
        )
        busy_times = busy_slots.get("calendars", {}).get("primary", {}).get("busy", [])
        if not busy_times:
            return "No busy slots found."
        return "\n".join(
            f"Busy from {format_dt(slot['start'])} to {format_dt(slot['end'])}"
            for slot in busy_times
        )

    except HttpError as error:
        return f"An error occurred: {error}"


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({"status": "healthy"})


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="streamable-http")
else:
    # Expose ASGI app for uvicorn
    app = mcp
