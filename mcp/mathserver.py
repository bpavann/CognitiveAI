from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Math")

@mcp.tool()
def add(a:int,b:int)->int:
    """ Add two number"""
    return a+b

@mcp.tool()
def mul(a:int,b:int)->int:
    """Multiply two number"""
    return a*b


# The TRANSPORT="STDIO" argument tells the server to:
# Use standard INPUT_OUTPUT (stdin and stdout) to receive and respond to tool function calls

if __name__=="__main__":
    mcp.run(transport="stdio")
