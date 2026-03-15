from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class TripPlanRequest(BaseModel):
    from_city: str = Field(
        min_length=1,
        strip=True,
        description="Город отправления"
    )
    to_city: str = Field(
        min_length=1,
        strip=True,
        description="Город прибытия"
    )
    days: int = Field(
        ge=1,
        le=30,
        description="Количество дней путешествия (1–30)"
    )
    budget: float = Field(
        gt=0,
        description="Бюджет на поездку (> 0)"
    )
    interests: List[str] = Field(
        max_items=10,
        description="Интересы путешественника (макс. 10)"
    )
    pace: Literal['calm', 'moderate', 'active'] = Field(
        description="Темп путешествия: спокойный, умеренный, активный"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Дополнительные заметки"
    )
