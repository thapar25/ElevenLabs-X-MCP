import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from dotenv import load_dotenv
import os

load_dotenv()


async def interact():
    try:
        transport = StreamableHttpTransport(
            url="http://127.0.0.1:8000/mcp/", auth=f"{os.getenv('TEST_TOKEN')}"
        )
        print("Using token:" + "*" * 5 + os.getenv("TEST_TOKEN")[-5:] + "\n")
        async with Client(transport=transport) as client:
            await client.ping()
            print("Ping successful!")

            # List available tools to confirm greet is available
            tools = await client.list_tools()
            print("Available tools:", tools)

            # # Call the greet tool using call_tool method
            # # Pass parameters as a dictionary instead
            tool_response = await client.call_tool("list_events", {"start": "2025-07-28", "end": "2025-07-30T23:59:59Z"})
            # tool_response = await client.call_tool("get_events_today", {})
            print("Result:", tool_response)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(interact())
