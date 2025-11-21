
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import Any
import os,json
import asyncio
from mcp_use import MCPAgent, MCPClient

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("Missing GROQ_API_KEY in .env")

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

async def setup_agent(message): 
    
    base_dir = os.path.dirname(__file__)
    server_path = os.path.abspath( os.path.join(base_dir, "../server/server.py"))
    config = {
        # "master_mcp": {
        #     "url": "http://localhost:8000/mcp",
        #     "transport": "streamable_http"
        # }
       "mcpServers": {
            "server":{
                "command":"python",
                "args":[server_path],
                "transport": "stdio",
            }        
        }
    }

    print(server_path)

    client = MCPClient(config=config)
    llm =  ChatGroq(model="qwen/qwen3-32b")
    agent = MCPAgent(llm=llm, client=client)

    result = await agent.run(message)
    return result