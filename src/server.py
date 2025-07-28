import argparse
from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from auth import auth_provider
from calendar_services import (
    fetch_busy_slots,
    fetch_events,
    create_calendar_event,
    update_calendar_event,
    delete_calendar_event,
)

_ = load_dotenv()

mcp = FastMCP(name="Google Calendar", auth=auth_provider, log_level="DEBUG", debug=True)


@mcp.tool()
async def get_busy_slots(start: str, end: str) -> str:
    """
    Get busy slots in the user's Google Calendar between start and end.
    Args:
        start (str): Start time in ISO 8601 (IST)
        end (str): End time in ISO 8601 (IST)
    Returns:
        All busy slots in ISO 8601 format (IST).
    """
    return await fetch_busy_slots(start, end)


@mcp.tool()
async def list_events(start: str, end: str) -> str:
    """
    List events in the user's Google Calendar between start and end.
    Args:
        start (str): Start time in ISO 8601 (IST)
        end (str): End time in ISO 8601 (IST)
    Returns:
        All events in ISO 8601 format (IST).
    """
    return await fetch_events(start, end)


@mcp.tool()
async def create_event(
    duration: str, temporal_information: str, event_description: str
) -> str:
    """
    Create an event in the user's Google Calendar based on information about the event (duration, day of the week, time of the day etc.).
    Eg:
        create_event("1 hour", "Monday at 10 AM", "Doctor's appointment")
        create_event("3 hours", "Last Saturday of the month at 8 PM","Family dinner in Mumbai")
    """
    return await create_calendar_event(
        duration, temporal_information, event_description
    )


@mcp.tool()
async def update_event(
    event_id: str, duration: str, temporal_information: str, event_description: str
) -> str:
    """
    Update an existing event in the user's Google Calendar.
    Args:
        event_id (str): The ID of the event to update.
        duration (str): New duration for the event.
        temporal_information (str): New temporal information for the event.
        event_description (str): New description for the event.
    Returns:
        str: Confirmation message or error message.
    """
    return await update_calendar_event(
        event_id, duration, temporal_information, event_description
    )


@mcp.tool()
async def delete_event(event_id: str) -> str:
    """
    Delete an existing event in the user's Google Calendar.
    Args:
        event_id (str): The ID of the event to delete.
    Returns:
        str: Confirmation message or error message.
    """
    return await delete_calendar_event(event_id)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """
    Health check endpoint to verify server status.
    Returns:
        JSONResponse: A JSON response indicating the server status.
    """
    return JSONResponse({"status": "healthy"})


def main():
    """
    Main function to run the FastMCP server.
    Parses command-line arguments to configure the transport method and server host/port.
    """
    parser = argparse.ArgumentParser(
        description="Run the FastMCP server with a specified transport."
    )
    parser.add_argument(
        "--transport",
        type=str,
        default="streamable-http",
        help="Specify the transport method (e.g., 'streamable-http', 'stdio', 'sse'). Default is 'streamable-http'.",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host for streamable-http transport. Default is 127.0.0.1.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for streamable-http transport. Default is 8000.",
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport=args.transport)
    else:
        mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
else:
    # Expose ASGI app for uvicorn
    app = mcp
