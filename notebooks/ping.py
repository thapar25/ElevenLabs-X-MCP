import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from dotenv import load_dotenv
import os

load_dotenv()


async def example():
    transport = StreamableHttpTransport(
        url="http://127.0.0.1:8000/mcp/", auth=f"Bearer {os.getenv('SECRET')}"
    )
    async with Client(transport=transport) as client:
        await client.ping()
        print("Ping successful!")

        # List available tools to confirm greet is available
        tools = await client.list_tools()
        print("Available tools:", tools)

        # # Call the greet tool using call_tool method
        # # Pass parameters as a dictionary instead
        # tool_response = await client.call_tool("get_busy_slots", {"start_time": "2025-05-01", "end_time": "2025-07-01T23:59:59Z"})
        tool_response = await client.call_tool("get_events_today", {})
        print("Result:", tool_response)


if __name__ == "__main__":
    asyncio.run(example())
