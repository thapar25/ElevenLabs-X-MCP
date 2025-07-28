from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from time_utils import to_ist_iso8601, parse_iso8601_to_ist
from auth import get_credentials


async def get_calendar_service():
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)


async def fetch_busy_slots(start: str, end: str) -> str:
    try:
        service = await get_calendar_service()
        response = (
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
        busy_times = response.get("calendars", {}).get("primary", {}).get("busy", [])
        if not busy_times:
            return "No busy slots found."
        return "\n".join(
            f"Busy from {to_ist_iso8601(parse_iso8601_to_ist(slot['start']))} to {to_ist_iso8601(parse_iso8601_to_ist(slot['end']))}"
            for slot in busy_times
        )
    except HttpError as error:
        return f"An error occurred: {error}"


async def fetch_events(start: str, end: str) -> str:
    try:
        service = await get_calendar_service()
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
            f"Event ID: {event['id']} - {event['summary']} at {to_ist_iso8601(parse_iso8601_to_ist(event['start'].get('dateTime', event['start'].get('date'))))}"
            for event in events
        )
    except HttpError as error:
        return f"An error occurred: {error}"


async def create_calendar_event(
    duration: str, temporal_info: str, description: str
) -> str:
    try:
        service = await get_calendar_service()
        event = (
            service.events()
            .quickAdd(
                calendarId="primary",
                text=f"{description} for {duration} on {temporal_info}",
            )
            .execute()
        )
        return f"Event created/updated: {event}"
    except HttpError as error:
        return f"An error occurred: {error}"


async def update_calendar_event(
    event_id: str, duration: str, temporal_info: str, description: str
) -> str:
    try:
        service = await get_calendar_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return await create_calendar_event(duration, temporal_info, description)
    except HttpError as error:
        return f"An error occurred: {error}"


async def delete_calendar_event(event_id: str) -> str:
    try:
        service = await get_calendar_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return f"Event with ID {event_id} deleted successfully."
    except HttpError as error:
        return f"An error occurred: {error}"
