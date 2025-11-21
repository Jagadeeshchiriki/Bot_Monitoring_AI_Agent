# main.py
from fastapi import FastAPI
from agent.client.client import setup_agent
from agent.server.api.jobs import get_job_by_id, get_logs_by_execution_id, get_rca_by_id

app = FastAPI()

@app.post("/v1/event")
async def read_root(jobid: str):
    job = get_job_by_id(jobid)
    logs = get_logs_by_execution_id(job["execution_id"])
    rca = get_rca_by_id(job["rca_id"])

    message = f"""
    JOB: {job}
    LOGS: {logs}
    RCA: {rca}
    """

    response = await setup_agent(message)
    return response


if __name__ == "__main__":
    import uvicorn
    # NOTE: uvicorn --reload spawns subprocesses; be mindful if your MCP child process
    # is started automatically from agent.client — you may get double-spawn behavior.
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
