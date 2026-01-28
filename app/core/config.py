from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    app_name: str
    env: str
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    # Database settings
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str = ""

    @property
    def database_url(self):
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"

settings = Settings()
