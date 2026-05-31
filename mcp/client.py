from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"],
                "transport":"stdio"            
                },
                "weather":{   
                    "url":"http://127.0.0.1:8000/mcp",
                    "transport":"streamable_http"
                }
        }
    )
    tools=await client.get_tools()
    print("Tools areready to bind with llm")
    llm=ChatOllama(model="llama3.1")
    agent=create_agent(llm,tools)

    math_response= await agent.ainvoke({"messages":[{"role":"user","content":"What is (3+5)*12 ?"}]})
    print(math_response["messages"][-1].content)
    print("\n\n")
    weat_response= await agent.ainvoke({"messages":[{"role":"user","content":"What is the weather in New Delhi ?"}]})
    print("Weather Response:",weat_response["messages"][-1].content)
asyncio.run(main())