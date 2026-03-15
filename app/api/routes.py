from fastapi import APIRouter, HTTPException
from app.schemas.request import TripPlanRequest
from app.schemas.response import TripPlanResponse
from app.schemas.error import ErrorResponse
from app.services.trip_service import generate_trip_plan

router = APIRouter()

@router.post("/plan-trip", response_model=TripPlanResponse, responses={400: {"model": ErrorResponse}})
async def plan_trip(request: TripPlanRequest):
    try:
        trip_plan = await generate_trip_plan(request)
        return trip_plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))