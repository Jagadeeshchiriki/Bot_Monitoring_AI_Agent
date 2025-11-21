import requests
import json
import os   
from dotenv import load_dotenv  
import pandas as pd
import re
from master_agent.agent.server.api.jobs import update_job


excel_path = r"C:\Users\vishesh\Downloads\RCA_Knowledge_Base.xlsx"



def rca_analyizer(Process_Name: str, State: str, Exception_Message: str):
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
        Base_Confidence = row['Base_Confidence']
        update_job(RCA_ID)

        # Add more columns here if needed
        return {'RCA_ID':RCA_ID, 'Base_Confidence':Base_Confidence}
    else:
        return None, None  # or raise an error if no match

# Example usage
rca_id, confidence = rca_analyizer(
    "TDECU_Insurance_Disbursement", 
    "Faulted", 
    "DNA Application Login failed"
)


# print("RCA_ID:", rca_id)
# print("Base_Confidence:", confidence)



    
