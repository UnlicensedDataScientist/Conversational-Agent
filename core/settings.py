# config.py
from pydantic import Field
from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    # Gemini API KEY
    gemini_api_key: str = Field(..., env="GEMINi_API_KEY")
    google_cloud_credentials: dict = Field(..., env="GOOGLE_CLOUD_CREDENTIALS")
    
    debug_level: str = "INFO"

    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8" 

settings = Settings()