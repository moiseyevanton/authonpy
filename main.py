from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import engine,SessionLocal, get_db
import models, schemas, auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
def seed_default_employer():
    db = SessionLocal()
    try:
        if not db.query(models.Employer).first():
            db.add(models.Employer(
                full_name="Test",
                password_hash=auth.hash_password("testpassword")
            ))
            db.commit()
    finally:
        db.close()


@app.post("/register/administrator", summary="Регистрация администратора", response_model=schemas.TokenResponse)
def register_admin(
    admin: schemas.AdministratorRegister,
    db: Session = Depends(get_db)
):
    # TODO: Проверка уникальности full_name во всех таблицах, с этим надо че то решить
    if (
        db.query(models.Employer).filter(models.Employer.full_name == admin.full_name).first() or
        db.query(models.Administrator).filter(models.Administrator.full_name == admin.full_name).first() or
        db.query(models.Worker).filter(models.Worker.full_name == admin.full_name).first()
    ):
        raise HTTPException(status_code=400, detail="Username already taken")

    # Проверка существования работодателя
    employer = db.query(models.Employer).filter(models.Employer.ID_employer == admin.ID_employer).first()
    if not employer:
        raise HTTPException(status_code=400, detail="Employer not found")

    new_admin = models.Administrator(
        full_name=admin.full_name,
        password_hash=auth.hash_password(admin.password),
        ID_employer=admin.ID_employer
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    token = auth.create_token({
        "sub": new_admin.full_name,
        "role": "administrator",
        "user_id": new_admin.ID_administrator
    })
    return {
        "access_token": token,
        "role": "administrator",
        "user_id": new_admin.ID_administrator
    }


@app.post("/register/worker", summary="Регистрация работника", response_model=schemas.TokenResponse)
def register_worker(
    worker: schemas.WorkerRegister,
    db: Session = Depends(get_db)
):
    # TODO: Проверка уникальности full_name во всех таблицах, с этим надо че то решить
    if (
        db.query(models.Employer).filter(models.Employer.full_name == worker.full_name).first() or
        db.query(models.Administrator).filter(models.Administrator.full_name == worker.full_name).first() or
        db.query(models.Worker).filter(models.Worker.full_name == worker.full_name).first()
    ):
        raise HTTPException(status_code=400, detail="Username already taken")

    # Проверка существования магазина
    store = db.query(models.Store).filter(models.Store.ID_store == worker.ID_store).first()
    if not store:
        raise HTTPException(status_code=400, detail="Store not found")

    # Если указан ID_administrator, проверяем его существование
    if worker.ID_administrator is not None:
        admin = db.query(models.Administrator).filter(
            models.Administrator.ID_administrator == worker.ID_administrator
        ).first()
        if not admin:
            raise HTTPException(status_code=400, detail="Administrator not found")

    new_worker = models.Worker(
        full_name=worker.full_name,
        password_hash=auth.hash_password(worker.password),
        ID_store=worker.ID_store,
        ID_administrator=worker.ID_administrator
    )
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)

    token = auth.create_token({
        "sub": new_worker.full_name,
        "role": "worker",
        "user_id": new_worker.ID_worker
    })
    return {
        "access_token": token,
        "role": "worker",
        "user_id": new_worker.ID_worker
    }


@app.post("/login", summary="Авторизация", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Последовательный поиск по всем таблицам
    employer = db.query(models.Employer).filter(models.Employer.full_name == user.full_name).first()
    if employer and auth.verify_password(user.password, employer.password_hash):
        token = auth.create_token({
            "sub": employer.full_name,
            "role": "employer",
            "user_id": employer.ID_employer
        })
        return {
            "access_token": token,
            "role": "employer",
            "user_id": employer.ID_employer
        }

    admin = db.query(models.Administrator).filter(models.Administrator.full_name == user.full_name).first()
    if admin and auth.verify_password(user.password, admin.password_hash):
        token = auth.create_token({
            "sub": admin.full_name,
            "role": "administrator",
            "user_id": admin.ID_administrator
        })
        return {
            "access_token": token,
            "role": "administrator",
            "user_id": admin.ID_administrator
        }

    worker = db.query(models.Worker).filter(models.Worker.full_name == user.full_name).first()
    if worker and auth.verify_password(user.password, worker.password_hash):
        token = auth.create_token({
            "sub": worker.full_name,
            "role": "worker",
            "user_id": worker.ID_worker
        })
        return {
            "access_token": token,
            "role": "worker",
            "user_id": worker.ID_worker
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )


@app.get("/me", response_model=schemas.UserProfile)
async def read_profile(
    current_user = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    profile = {
        "full_name": current_user.full_name,
        "role": current_user.role,
        "additional_info": {}
    }
    # Дополнительные данные в зависимости от роли
    if current_user.role == "employer":
        # ничего особо нет
        pass
    elif current_user.role == "administrator":
        profile["additional_info"]["ID_employer"] = current_user.ID_employer
    elif current_user.role == "worker":
        profile["additional_info"]["ID_store"] = current_user.ID_store
        profile["additional_info"]["ID_administrator"] = current_user.ID_administrator

    return profile