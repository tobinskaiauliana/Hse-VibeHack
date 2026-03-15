from app.schemas.request import TripPlanRequest
from app.schemas.response import TripPlanResponse
from app.services.validation_service import validate_and_normalize
from app.services.prompt_service import build_trip_prompt
from app.services.llm_service import call_llm, parse_llm_response
from app.core.logger import logger

def generate_trip_plan(request_data: TripPlanRequest) -> TripPlanResponse:
    normalized_data = validate_and_normalize(request_data)
    prompt = build_trip_prompt(normalized_data)
    raw_response = call_llm(prompt)
    if not raw_response:
        raise Exception("Failed to get response from LLM")
    parsed_response = parse_llm_response(raw_response)
    if not parsed_response:
        parsed_response = {
            "summary": "Could not generate detailed plan due to AI processing error",
            "budget": {"housing": 0, "food": 0, "transport": 0, "activities": 0},
            "days": [{"day": 1, "title": "Travel Day", "description": "Start your journey"}],
            "tips": ["Check official travel guides for more information"],
            "warnings": ["AI response parsing failed, using fallback plan"]
        }

    try:
        return TripPlanResponse(**parsed_response)
    except Exception as e:
        logger.error(f"Failed to validate response structure: {e}")
        raise
