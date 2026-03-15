#требуется подключить платную нейросеть, удобнее работать с openai
def build_trip_prompt(trip_data: dict) -> str:
    system_prompt = """
You are an expert travel planner with access to real-time travel data.
Your task is to create a detailed, actionable travel itinerary.
Return response STRICTLY in valid JSON format.
Include specific recommendations for transportation, accommodation, and activities.
"""

    user_prompt = f"""
Create a comprehensive travel plan from {trip_data['from_city']} to {trip_data['to_city']}.

Trip Parameters:
- Duration: {trip_data['days']} days
- Budget: {trip_data['budget']} RUB
- Interests: {', '.join(trip_data['interests'])}
- Pace: {trip_data['pace']}
- Additional Notes: {trip_data.get('notes', 'None')}

Include the following details in the plan:

Daily Schedule:
- Specific transportation options (flights/trains/buses) with estimated costs
- Accommodation recommendations with prices
- Activity planning with timing and costs
- Meal suggestions with budget allocation

Detailed Structure:
- summary: brief assessment of trip feasibility
- budget_breakdown:
  - housing: daily budget for accommodation
  - food: daily budget for meals
  - transport: daily budget for local transport
  - activities: daily budget for attractions
- itinerary:
  - for each day:
    - day_number
    - arrival_transport: details of transportation to destination
    - accommodation: hotel/hostel/apartment details
    - schedule:
      - time_blocks with activities
      - estimated costs
      - transportation between points
- recommendations:
  - best times for activities
  - local tips
  - safety advice
- warnings:
  - potential issues
  - contingency plans
  - emergency contacts

Constraints:
- Total budget must not exceed {trip_data['budget']} RUB
- Allocate budget realistically across categories
- Consider realistic travel times between locations
- Include buffer time for unexpected delays
- Provide alternative options where possible

Format response as valid JSON with the following structure:
{{
    "summary": "string",
    "budget_breakdown": {
        "housing": float,
        "food": float,
        "transport": float,
        "activities": float
    },
    "itinerary": [
        {
            "day_number": int,
            "arrival_transport": {
                "type": "string",
                "departure_time": "HH:MM",
                "arrival_time": "HH:MM",
                "cost": float
            },
            "accommodation": {
                "name": "string",
                "address": "string",
                "price_per_night": float,
                "booking_link": "string"
            },
            "schedule": [
                {
                    "time_block": "HH:MM-HH:MM",
                    "activity": "string",
                    "location": "string",
                    "cost": float,
                    "transport_to": "string"
                }
            ]
        }
    ],
    "recommendations": ["string"],
    "warnings": ["string"]
}}
"""
    return f"{system_prompt}\n\n{user_prompt}"