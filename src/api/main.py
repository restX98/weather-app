import csv

import openmeteo_requests
import pandas as pd
import requests_cache
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from retry_requests import retry
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Location

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def seed_data():
    print("Startup")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if not db.query(Location).first():
            csv_path = "data/locations.csv"

            locations = []

            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    print(row)
                    locations.append(
                        Location(
                            name=row["Capital City"],
                            latitude=float(row["Latitude"]),
                            longitude=float(row["Longitude"]),
                        ),
                    )

            db.add_all(locations)
            db.commit()
    finally:
        db.close()


@app.get("/")
def good_luck():
    return {
        "Good": "Luck!",
    }


def map_weather_code_to_icon_key(code: int) -> str:
    if code == 0:
        return "sun"  # ☀️
    elif code in (1, 2):
        return "sun-cloud"  # 🌤️
    elif code in (3, 45, 48):
        return "cloud"  # ☁️
    elif code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 71, 73, 75, 77, 80, 81, 82, 85, 86):
        return "rain-sun"  # 🌦️
    elif code in (95, 96, 99):
        return "thunder"  # ⛈️
    else:
        return "unknown"


@app.get("/locations")
def get_locations(db: Session = Depends(get_db)):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": None, "longitude": None, "current": ["temperature_2m", "precipitation", "weather_code"]}

    locations = db.query(Location).all()
    result = []

    for loc in locations:
        params["latitude"] = loc.latitude
        params["longitude"] = loc.longitude
        responses = openmeteo.weather_api(url, params=params)
        current = responses[0].Current()

        temperature = current.Variables(0).Value()
        precipitation = current.Variables(1).Value()
        weather_code = current.Variables(2).Value()
        result.append(
            {
                "id": loc.id,
                "name": loc.name,
                "temperature": f"{temperature:.0f} °C",
                "rain": f"{precipitation:.0f} mm",
                "status": map_weather_code_to_icon_key(weather_code),
            },
        )

    return result
