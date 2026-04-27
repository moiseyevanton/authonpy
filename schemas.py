from pydantic import BaseModel
from typing import Optional

# --- Запросы на регистрацию ---
class AdministratorRegister(BaseModel):
    full_name: str
    password: str
    ID_employer: int

class WorkerRegister(BaseModel):
    full_name: str
    password: str
    ID_store: int
    ID_administrator: Optional[int] = None

# --- Запрос на авторизацию ---
class UserLogin(BaseModel):
    full_name: str
    password: str

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