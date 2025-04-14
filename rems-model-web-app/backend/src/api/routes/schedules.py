from fastapi import APIRouter, HTTPException
from ..services.google_sheets_service import GoogleSheetsService
from pydantic import BaseModel
from typing import Optional, List
import json
import pandas as pd


"""

"""
class SpreadsheetData(BaseModel):
    fileId: str
    authAccessToken: str


router = APIRouter(
    prefix= "/schedules",
    tags = ["Schedules"]
)

@router.post("/")
async def create_schedule(data: SpreadsheetData):

    # Step One: Parsing the google sheet into a dataframe
    google_sheets_service = GoogleSheetsService()
    df = google_sheets_service.create_scheduler_input_df(data.fileId, data.authAccessToken)


    # Step Two: Translating the dataframe into gurobi optimization model input

    # Step Three: Calling Schedule Optimizer service and getting raw outputs for scheduling

    # Step Four: Translating uninterpretable model outputs to name, email, timeslots of shift scheduled,
    # etc for calendar view and gcal invites

    
    print(df.columns)

    print(data.fileId)
    print(data.authAccessToken)
