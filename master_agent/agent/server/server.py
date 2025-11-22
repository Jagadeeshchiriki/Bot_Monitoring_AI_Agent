# master_mcp_server.py
from mcp.server.fastmcp import FastMCP
import requests
import json
import asyncio
import smtplib
from tools.rca import get_rca_response

mcp = FastMCP("server")

# ---- SOP/RCA Lookup Tool ----
print("Server starting...")

url = "http://localhost:8001/send_email"


@mcp.tool()
async def get_rca(jobid:str) -> dict:
    """
    Query knowledge base for exception resolution confidence.
    """
    rca_response= await get_rca_response(jobid)
  
    return rca_response
    

# ---- Action Executor Tool ----
@mcp.tool()
def send_mail(action: str, payload: dict) -> dict:
    """
    Send the mail to developer with exception message and get  the approval response.
    action:action_request
    payload:{
        JobID,
        ErrorType,
        Message
        action_request
    }
    """
    data={ 
     "payload": {
        "JobId": payload["JobID"],
        "ErrorType": payload["ErrorType"],
        "Message": payload["Message"],
        "action_request":payload["action_request"]
    },
    "threadId": "abc123-thread"
   }
    response = requests.post(url, json=data)

    # Check response
    if response.status_code == 200:
        print("Email triggered successfully!")
        print(response.json())
    else:
        print("Failed to trigger endpoint:", response.status_code, response.text)
        

# ---- Audit Logging Tool ----
@mcp.tool()
def perform_action(event: str, data: dict) -> dict:
    """
    Log event for traceability.
    """
    print(f"[AUDIT] {event} :: {data}")
    return {"status": "logged"}


if __name__ == "__main__":
    mcp.run()
