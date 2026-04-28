from pydantic import BaseModel
from typing import Optional


# --- Запрос на авторизацию ---
class UserLogin(BaseModel):
    full_name: str
    password: str


# --- Запросы на регистрацию ---
class AdministratorRegister(UserLogin):
    ID_employer: int


class WorkerRegister(UserLogin):
    ID_store: int
    ID_administrator: Optional[int] = None


# --- Ответ с токеном ---
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int


# --- Профиль пользователя (для /me) ---
class UserProfile(BaseModel):
    full_name: str
    role: str
    additional_info: Optional[dict] = {}