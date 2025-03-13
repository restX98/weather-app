import csv

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Location

Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/locations")
def get_locations(db: Session = Depends(get_db)):
    locations = db.query(Location).all()
    result = [
        {
            "id": loc.id,
            "name": loc.name,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
        }
        for loc in locations
    ]
    return result
