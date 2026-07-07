from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    virustotal_api_key: str | None = None
    abuseipdb_api_key: str | None = None
    database_url: str = "sqlite:///./ioc_agent.db"
    cache_ttl_hours: int = 24
    abuseipdb_max_age_days: int = 90
    # fastapi_base_url: str = "http://api:8000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
