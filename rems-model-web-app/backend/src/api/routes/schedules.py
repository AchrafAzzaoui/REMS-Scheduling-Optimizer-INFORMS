from fastapi import APIRouter, HTTPException, Request
from ..services.google_sheets_service import GoogleSheetsService
from pydantic import BaseModel
from typing import Optional, List
import json
import pandas as pd


"""

"""
class SpreadsheetData(BaseModel):
    fileId: str



router = APIRouter(
    prefix= "/schedules",
    tags = ["Schedules"]
)

@router.post("/")
async def create_schedule(request:Request, data: SpreadsheetData):

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    auth_access_token = auth_header.split(" ")[1]
    # Step One: Parsing the google sheet into a dataframe
    google_sheets_service = GoogleSheetsService()
    df = google_sheets_service.create_scheduler_input_df(data.fileId, auth_access_token)
    # Step Two: Translating the dataframe into gurobi optimization model input

    # Step Three: Calling Schedule Optimizer service and getting raw outputs for scheduling

    # Step Four: Translating uninterpretable model outputs to name, email, timeslots of shift scheduled,
    # etc for calendar view and gcal invites

    
    print(df.columns)

    print(data.fileId)
