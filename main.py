from fastapi import FastAPI
from db.db import engine,SessionLocal, get_db
import models.models as models, jwt.jwt as jwt
from api.api import router


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def seed_default_data():
    db = SessionLocal()
    try:
        # Создаём тестового работодателя, если нет
        employer = db.query(models.Employer).filter(
            models.Employer.username == "Test"
        ).first()
        
        if not employer:
            employer = models.Employer(
                username="Test",
                first_name="Test",
                last_name="Test",
                password_hash=jwt.hash_password("testpassword")
            )
            db.add(employer)
            db.commit()
            db.refresh(employer)

        # Создаём тестовый магазин, если нет
        store = db.query(models.Store).filter(
            models.Store.name == "Test Store"
        ).first()
        
        if not store:
            store = models.Store(
                name="Test Store",
                address="Test Address, 123",
                ID_employer=employer.ID_employer
            )
            db.add(store)
            db.commit()
            db.refresh(store)

    finally:
        db.close()
