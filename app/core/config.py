from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name:str="Mini Store"
    app_version:str="1.0.0"
    debug:bool=True

    database_url:str="sqlite:///./store.db"

    jwt_secret_key:str="5a2b4625efe619c2038ecb6da5c2f91675ffbb4f4befb115021f79ad9e20e200"
    jwt_algorithm:str="HS256"
    access_token_expire_minutes:int=30

    allowed_origin:str="http://localhost:3000,http://localhost:5173"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")

    @property
    def cors_origin(self)->list[str]:
        o=[origin.strip() for origin in self.allowed_origin.split(",") if origin.strip()]

        return o

@lru_cache
def get_settings()->Settings:
    return Settings()

settings=get_settings()