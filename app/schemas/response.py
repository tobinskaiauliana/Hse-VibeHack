from pydantic import BaseModel
from typing import List

class BudgetBreakdown(BaseModel):
    housing: float
    food: float
    transport: float
    activities: float

class DayPlan(BaseModel):
    day: int
    title: str
    description: str

class TripPlanResponse(BaseModel):
    summary: str
    budget: BudgetBreakdown
    days: List[DayPlan]
    tips: List[str]
    warnings: List[str] = []