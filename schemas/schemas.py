from pydantic import BaseModel
from typing import Optional


# --- Запрос на авторизацию ---
class UserLogin(BaseModel):
    username: str
    password: str
    ip_address: str


# --- Запросы на регистрацию ---
class AdministratorRegister(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    ID_employer: int
    ip_address: str


class WorkerRegister(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    ID_store: int
    ID_administrator: Optional[int] = None
    ip_address: str


# --- Ответ с токеном ---
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int


# --- Профиль пользователя (для /me) ---
class UserProfile(BaseModel):
    username: str
    first_name: str
    last_name: str
    role: str
    additional_info: Optional[dict] = {}