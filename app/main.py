
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import (
    initialize_database,
    add_search,
    get_history,
    add_favorite,
    remove_favorite,
    get_favorites,
)

from app.weather_service import find_city, get_weather


app = FastAPI(
    title="Weather Intelligence Dashboard",
    description="Weather information and search history API",
    version="1.0.0"
)


class CityRequest(BaseModel):
    city: str


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
def home():
    return {
        "message": "Weather Intelligence Dashboard API is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/weather")
def weather(city: str):
    try:
        location = find_city(city)

        if not location:
            raise HTTPException(
                status_code=404,
                detail="City not found"
            )

        weather_data = get_weather(
            location["latitude"],
            location["longitude"]
        )

        add_search(city)

        return {
            "location": location,
            "weather": weather_data
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/history")
def history():
    return get_history()


@app.get("/favorites")
def favorites():
    return get_favorites()


@app.post("/favorites")
def save_favorite(request: CityRequest):
    add_favorite(request.city)

    return {
        "message": "Favorite added successfully",
        "city": request.city
    }


@app.delete("/favorites/{city}")
def delete_favorite(city: str):
    remove_favorite(city)

    return {
        "message": "Favorite removed successfully",
        "city": city
    }
