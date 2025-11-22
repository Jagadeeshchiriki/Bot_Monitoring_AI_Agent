import requests
import json
import os  
import datetime
from dotenv import load_dotenv  
import pandas as pd
import re
from api.jobs import update_job,get_execution_by_executionid,get_logs_by_execution_id,get_job_by_id


excel_path = r"C:\Users\vishesh\Downloads\RCA_Knowledge_Base.xlsx"


async def rca_analyizer(Process_Name: str, State: str, Exception_Message: str):
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Filter the row that matches all three inputs
    filtered_df = df[
        (df['Process_Name'] == Process_Name) &
        (df['State'] == State) &
        (df['Exception_Message'] == Exception_Message)
    ]
    
    if not filtered_df.empty:
        # Directly get the values from the first matching row
        row = filtered_df.iloc[0]  # pick the first match
        RCA_ID = row['RCA_ID']
        Suggested_Action=row['Suggested_Action']
        Base_Confidence = row['Base_Confidence']
        
        result={'RCA_ID':RCA_ID, 'Suggested_Action':Suggested_Action,'Base_Confidence':Base_Confidence}
        # Add more columns here if needed
        return result
    else:
        return None, None  # or raise an error if no match


async def get_rca_response(jobid: str):
    job = await get_job_by_id(jobid)
    if not job:
        raise ValueError("Job not found")

    logs = await get_logs_by_execution_id(job["ExecutionId"])
    if not logs:
        raise ValueError("No logs found")

    execution = await get_execution_by_executionid(job["ExecutionId"])
    if not execution:
        raise ValueError("Execution details not found")

    try:
        Exception_Message = max(
            logs,
            key=lambda x: datetime.fromisoformat(x["dateTime"])
        )
    except Exception as e:
        raise ValueError(f"Error parsing logs: {e}")

    return await rca_analyizer(
        execution['Process_Name'],
        execution['State'],
        Exception_Message
    )
 











# Example usage
# rca_id, Suggested_Action,confidence  = rca_analyizer(
#     "TDECU_Insurance_Disbursement", 
#     "Faulted", 
#     "DNA Application Login failed"
# )


# print("RCA_ID:", rca_id)
# print("Base_Confidence:", confidence)



    
