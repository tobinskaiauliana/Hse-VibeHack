import requests
import time
from typing import List, Dict, Optional
from fastapi import HTTPException
from datetime import datetime

def get_city_coordinates(city: str, country: str = "") -> Optional[tuple]:
    url = "https://nominatim.openstreetmap.org/search"
    query_parts = [city]
    if country:
        query_parts.append(country)
    query = ", ".join(query_parts)

    params = {
        "format": "json",
        "q": query,
        "limit": 1
    }
    headers = {"User-Agent": "TravelPlanner/2.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"Ошибка геокодирования: {e}")
    return None, None

def get_nearby_places(lat: float, lon: float, query: str = "attraction", limit: int = 5) -> List[Dict]:
    url = "https://nominatim.openstreetmap.org/search"
    delta = 0.15
    params = {
        "format": "json",
        "q": query,
        "viewbox": f"{lon-delta},{lat-delta},{lon+delta},{lat+delta}",
        "bounded": 1,
        "limit": limit * 3,
        "addressdetails": 1
    }
    headers = {"User-Agent": "TravelPlanner/2.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()

        attractions = []
        for place in data:
            name = place.get("name", "Без названия")
            if name == "Без названия":
                continue

            category = place.get("category", "N/A")
            type_val = place.get("type", "N/A")
            full_type = f"{category}/{type_val}" if type_val != "N/A" else category

            attractions.append({
                "name": name,
                "type": full_type,
                "address": place.get("display_name", "Адрес не указан"),
                "latitude": float(place.get("lat", 0)),
                "longitude": float(place.get("lon", 0))
            })

            if len(attractions) >= limit:
                break
        return attractions
    except Exception as e:
        print(f"OSM error: {e}")
        return []

def smart_search_by_interest(lat: float, lon: float, interest: str, days: int) -> List[Dict]:
    limit = max(2, min(days * 2, 10))

    queries = [
        interest,
        f"{interest} in {interest}" if interest else interest,
        "attraction",
        "landmark",
        "tourist_attraction"
    ]

    results = []
    seen_names = set()

    for i, query in enumerate(queries):
        if i > 0:
            time.sleep(1)

        current_results = get_nearby_places(lat, lon, query, limit)
        for item in current_results:
            if item["name"] not in seen_names:
                results.append(item)
                seen_names.add(item["name"])

        if len(results) >= limit:
            break

    return results[:limit]

def create_trip_plan(
    prompt: str,
    departure_city: str,
    arrival_city: str,
    country: str,
    start_date: str,
    end_date: str,
    budget: int,
    number_of_people: int,
    travel_style: str,
    interests: str
) -> Dict:
    lat, lon = get_city_coordinates(arrival_city, country)
    if not lat or not lon:
        raise HTTPException(
            status_code=400,
            detail=f"Город прибытия '{arrival_city}' не найден. Проверьте название и страну."
        )
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days

    if days <= 0:
        raise HTTPException(
            status_code=400,
            detail="Дата окончания должна быть позже даты начала"
        )

    interest_keywords = {
        "музей": "museum",
        "дворец": "palace",
        "собор": "cathedral",
        "храм": "temple",
        "святыня": "shrine",
        "памятник": "monument",
        "парк": "park",
        "галерея": "gallery",
        "замок": "castle",
        "аквапарк": "water park",
        "театр": "theater"
    }

    search_interest = "attraction"
    for key, value in interest_keywords.items():
        if key in interests.lower():
            search_interest = value
            break

    attractions = smart_search_by_interest(lat, lon, search_interest, days)

    budget_per_person = budget // number_of_people if number_of_people > 0 else 0

    recommended_per_day = max(1, len(attractions) // days) if days > 0 else 1

    return {
        "trip_overview": {
            "departure_city": departure_city,
            "arrival_city": arrival_city,
            "country": country,
            "start_date": start_date,
            "end_date": end_date,
            "duration_days": days,
            "budget_total": budget,
            "budget_per_person": budget_per_person,
            "number_of_people": number_of_people,
            "travel_style": travel_style,
            "interests": interests
        },
        "attractions_summary": {
            "total_found": len(attractions),
            "recommended_per_day": recommended_per_day,
            "attractions": attractions
        },
        "api_used": "OpenStreetMap"
    }
