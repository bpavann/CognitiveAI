from mcp.server.fastmcp import FastMCP

mcp=FastMCP("weather")

@mcp.tool()
async def get_weather(location:str)->str:
    """Get the weather of give location"""
    return f"Weather in the given is always Raining!!"

if __name__=="__main__":
    mcp.run(transport="streamable-http")
    