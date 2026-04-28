from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db import get_db
import models.models as models
import schemas.schemas as schemas
import jwt.jwt as jwt

router = APIRouter(tags=["api"])


def _authenticate_and_log_ip(
    db: Session,
    username: str,
    password: str,
    ip_address: str
) -> dict:
    """
    Ищет пользователя по всем трём таблицам.
    Если найден и пароль верный — записывает IP и возвращает словарь.
    Если не найден — возвращает None.
    """
    # Таблицы и роли: (модель, роль, id_attr)
    user_tables = [
        (models.Employer, "employer", "ID_employer"),
        (models.Administrator, "administrator", "ID_administrator"),
        (models.Worker, "worker", "ID_worker"),
    ]

    for model, role, id_attr in user_tables:
        user = db.query(model).filter(model.username == username).first()
        if user and jwt.verify_password(password, user.password_hash):
            # Сохраняем IP
            user_ip_data = {
                "ip_address": ip_address,
                f"ID_{role}": getattr(user, id_attr)
            }
            user_ip = models.UserIP(**user_ip_data)
            db.add(user_ip)
            db.commit()

            # Создаём токен
            token = jwt.create_token({
                "sub": user.username,
                "role": role,
                "user_id": getattr(user, id_attr)
            })
            return {
                "access_token": token,
                "role": role,
                "user_id": getattr(user, id_attr)
            }

    return None


@router.post("/register/administrator", summary="Регистрация администратора", response_model=schemas.TokenResponse)
def register_admin(
    admin: schemas.AdministratorRegister,
    db: Session = Depends(get_db)
):
    # Проверка уникальности username во всех таблицах
    if (
        db.query(models.Employer).filter(models.Employer.username == admin.username).first() or
        db.query(models.Administrator).filter(models.Administrator.username == admin.username).first() or
        db.query(models.Worker).filter(models.Worker.username == admin.username).first()
    ):
        raise HTTPException(status_code=400, detail="Username already taken")

    # Проверка существования работодателя
    employer = db.query(models.Employer).filter(models.Employer.ID_employer == admin.ID_employer).first()
    if not employer:
        raise HTTPException(status_code=400, detail="Employer not found")

    new_admin = models.Administrator(
        username=admin.username,
        first_name=admin.first_name,
        last_name=admin.last_name,
        password_hash=jwt.hash_password(admin.password),
        ID_employer=admin.ID_employer
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    # Сохраняем IP
    user_ip = models.UserIP(
        ip_address=admin.ip_address,
        ID_administrator=new_admin.ID_administrator
    )
    db.add(user_ip)
    db.commit()

    token = jwt.create_token({
        "sub": new_admin.username,
        "role": "administrator",
        "user_id": new_admin.ID_administrator
    })
    return {
        "access_token": token,
        "role": "administrator",
        "user_id": new_admin.ID_administrator
    }


@router.post("/register/worker", summary="Регистрация работника", response_model=schemas.TokenResponse)
def register_worker(
    worker: schemas.WorkerRegister,
    db: Session = Depends(get_db)
):
    # Проверка уникальности username во всех таблицах
    if (
        db.query(models.Employer).filter(models.Employer.username == worker.username).first() or
        db.query(models.Administrator).filter(models.Administrator.username == worker.username).first() or
        db.query(models.Worker).filter(models.Worker.username == worker.username).first()
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
        username=worker.username,
        first_name=worker.first_name,
        last_name=worker.last_name,
        password_hash=jwt.hash_password(worker.password),
        ID_store=worker.ID_store,
        ID_administrator=worker.ID_administrator
    )
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)

    # Сохраняем IP
    user_ip = models.UserIP(
        ip_address=worker.ip_address,
        ID_worker=new_worker.ID_worker
    )
    db.add(user_ip)
    db.commit()

    token = jwt.create_token({
        "sub": new_worker.username,
        "role": "worker",
        "user_id": new_worker.ID_worker
    })
    return {
        "access_token": token,
        "role": "worker",
        "user_id": new_worker.ID_worker
    }


@router.post("/login", summary="Авторизация", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    result = _authenticate_and_log_ip(
        db, user.username, user.password, user.ip_address
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return result

@router.get("/me", response_model=schemas.UserProfile)
async def read_profile(
    current_user = Depends(jwt.get_current_user),
    db: Session = Depends(get_db)
):
    profile = {
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
        "additional_info": {}
    }
    # Дополнительные данные в зависимости от роли
    if current_user.role == "employer":
        profile["additional_info"]["ID_employer"] = current_user.ID_employer
    elif current_user.role == "administrator":
        profile["additional_info"]["ID_employer"] = current_user.ID_employer
    elif current_user.role == "worker":
        profile["additional_info"]["ID_store"] = current_user.ID_store
        profile["additional_info"]["ID_administrator"] = current_user.ID_administrator

    return profile