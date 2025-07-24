import datetime
import pytz
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastmcp import FastMCP
from time_utils import to_ist_iso8601, parse_iso8601_to_ist
from auth import auth_provider, get_credentials
from dotenv import load_dotenv
from starlette.responses import JSONResponse


_ = load_dotenv()


mcp = FastMCP(name="Google Calendar", auth=auth_provider, log_level="DEBUG", debug=True)


@mcp.tool()
async def get_events_today() -> str:
    """
    Get today's events from the user's Google Calendar.
    All times are returned in ISO 8601 format (IST).
    """
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)
        now_ist = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        today_ist = now_ist.date()
        end_of_day_ist = datetime.datetime.combine(
            today_ist,
            datetime.time(23, 59, 59, 999999),
        )
        end_of_day_ist = parse_iso8601_to_ist(end_of_day_ist.isoformat())

        now_iso = to_ist_iso8601(now_ist)
        end_of_day_iso = to_ist_iso8601(end_of_day_ist)

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
            description = event.get("description", "No Description provided")
            start = to_ist_iso8601(parse_iso8601_to_ist(start_time))
            end = to_ist_iso8601(parse_iso8601_to_ist(end_time))
            response.append(
                f"Event: {title}\nDescription: {description}\nStart: {start}\nEnd: {end}"
            )
        return "\n".join(response)

    except HttpError as error:
        return f"An error occurred: {error}"


@mcp.tool()
async def get_busy_slots(start: str, end: str) -> str:
    """
    Get busy slots in the user's Google Calendar between start and end.
    Args:
        start (str): Start time in ISO 8601 (IST, no tzinfo)
        end (str): End time in ISO 8601 (IST, no tzinfo)
    Returns:
        All busy slots in ISO 8601 format (IST).
    """
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)
        busy_slots = (
            service.freebusy()
            .query(
                body={
                    "timeMin": to_ist_iso8601(parse_iso8601_to_ist(start)),
                    "timeMax": to_ist_iso8601(parse_iso8601_to_ist(end)),
                    "timeZone": "Asia/Kolkata",
                    "items": [{"id": "primary"}],
                }
            )
            .execute()
        )
        busy_times = busy_slots.get("calendars", {}).get("primary", {}).get("busy", [])
        if not busy_times:
            return "No busy slots found."
        return "\n".join(
            f"Busy from {to_ist_iso8601(parse_iso8601_to_ist(slot['start']))} to {to_ist_iso8601(parse_iso8601_to_ist(slot['end']))}"
            for slot in busy_times
        )

    except HttpError as error:
        return f"An error occurred: {error}"


@mcp.tool()
async def list_events(start: str, end: str) -> str:
    """
    List events in the user's Google Calendar between start and end.
    Args:
        start (str): Start time in ISO 8601 (IST, no tzinfo)
        end (str): End time in ISO 8601 (IST, no tzinfo)
    Returns:
        All events in ISO 8601 format (IST).
    """
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=to_ist_iso8601(parse_iso8601_to_ist(start)),
                timeMax=to_ist_iso8601(parse_iso8601_to_ist(end)),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        if not events:
            return "No upcoming events found."
        return "\n".join(
            f"{event['summary']} at {to_ist_iso8601(parse_iso8601_to_ist(event['start'].get('dateTime', event['start'].get('date'))))}"
            for event in events
        )

    except HttpError as error:
        return f"An error occurred: {error}"


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """Health check endpoint to verify server status.
    Returns:
        JSONResponse: A JSON response indicating the server status.
    """
    return JSONResponse({"status": "healthy"})


def main():
    """Main function to run the FastMCP server."""
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
else:
    # Expose ASGI app for uvicorn
    app = mcp
