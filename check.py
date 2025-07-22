import asyncio
from fastmcp import Client  # type: ignore
from fastmcp.client.transports import StreamableHttpTransport  # type: ignore

async def example():
    transport = StreamableHttpTransport("http://127.0.0.1:8000/mcp/")
    async with Client(transport=transport) as client:
        await client.ping()
        print("Ping successful!")

        # List available tools to confirm greet is available
        tools = await client.list_tools()
        print("Available tools:", tools)

        # # Call the greet tool using call_tool method
        # # Pass parameters as a dictionary instead
        tool_response = await client.call_tool("get_busy_slots", {"start_time": "2025-05-01", "end_time": "2025-07-01T23:59:59Z"})
        print("Result:", tool_response)

if __name__ == "__main__":
    asyncio.run(example())
