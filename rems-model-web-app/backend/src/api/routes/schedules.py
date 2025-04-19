from fastapi import APIRouter, HTTPException, Request
from ..services.google_sheets_service import GoogleSheetsService
from ..services.model_input_parser_service import ModelInputParserService
from ..services.gurobi_scheduler_optimizer_service import GurobiSchedulerOptimizerService
from pydantic import BaseModel
from typing import Dict, Optional, List
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
    df: pd.DataFrame = GoogleSheetsService.create_scheduler_input_df(data.fileId, auth_access_token)
    # Step Two: Translating the dataframe into gurobi optimization model input
    model_inputs: Dict[str, any] = ModelInputParserService.parse_df_to_model_input(df)

    names = model_inputs["names"]
    emails = model_inputs["emails"]
    role_statuses = model_inputs["role_statuses"]
    oc_statuses = model_inputs["oc_statuses"]
    availability = model_inputs["availability"]
    dates = model_inputs["dates"]
    # Step Three: Calling Schedule Optimizer service and getting raw outputs for scheduling
    gurobi_schedule_optimizer_service = GurobiSchedulerOptimizerService(**model_inputs)
    # Step Four: Translating uninterpretable model outputs to name, email, timeslots of shift scheduled,
    # etc for calendar view and gcal invites

    
    print(df.columns)

    print(data.fileId)
