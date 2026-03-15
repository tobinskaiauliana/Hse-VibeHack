from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.services.llm_service import create_trip_plan
from datetime import datetime

app = FastAPI(
    title="Travel Planner API",
    description="API для планирования путешествий",
    version="2.0.0"
)

class TripRequest(BaseModel):
    prompt: str = Field(
        default="Хочу посетить парки в Москве",
        description="Запрос пользователя с интересами и пожеланиями"
    )
    departure_city: str = Field(
        default="",
        description="Город отправления"
    )
    arrival_city: str = Field(
        default="Moscow",
        description="Город прибытия"
    )
    country: str = Field(
        default="Russia",
        description="Страна назначения"
    )
    start_date: str = Field(
        default="2026-03-15",
        description="Дата начала путешествия (YYYY-MM-DD)"
    )
    end_date: str = Field(
        default="2026-03-16",
        description="Дата окончания путешествия (YYYY-MM-DD)"
    )
    budget: int = Field(
        default=10000,
        ge=0,
        description="Бюджет на поездку в рублях"
    )
    number_of_people: int = Field(
        default=1,
        ge=1,
        description="Количество путешественников"
    )
    travel_style: str = Field(
        default="комфортный",
        description="Стиль путешествия: эконом, комфортный, люкс"
    )
    interests: str = Field(
        default="парки",
        description="Интересы путешественника: музеи, храмы, парки и т.д."
    )

@app.post("/plan-trip", response_model=dict)
async def plan_trip(request: TripRequest):
    try:
        start = datetime.strptime(request.start_date, "%Y-%m-%d")
        end = datetime.strptime(request.end_date, "%Y-%m-%d")
        if start >= end:
            raise HTTPException(
                status_code=400,
                detail="Дата начала должна быть раньше даты окончания"
            )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Неверный формат даты. Используйте YYYY-MM-DD"
        )

    if not request.arrival_city:
        raise HTTPException(
            status_code=400,
            detail="Необходимо указать город прибытия"
        )

    result = create_trip_plan(
        request.prompt,
        request.departure_city,
        request.arrival_city,
        request.country,
        request.start_date,
        request.end_date,
        request.budget,
        request.number_of_people,
        request.travel_style,
        request.interests
    )
    return result

@app.get("/")
def root():
    return {"message": "Travel Planner API"}