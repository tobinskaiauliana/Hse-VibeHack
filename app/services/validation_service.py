from app.schemas.request import TripPlanRequest
from app.core.logger import logger

def validate_and_normalize(data: TripPlanRequest) -> dict:
    if data.from_city.lower() == data.to_city.lower():
        raise ValueError("From city and to city must be different")

    normalized = data.dict()
    normalized['from_city'] = data.from_city.strip().title()
    normalized['to_city'] = data.to_city.strip().title()

    logger.info(f"Validated and normalized trip request: {normalized}")
    return normalized