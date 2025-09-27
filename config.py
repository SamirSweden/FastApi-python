from pydantic_settings import BaseSettings



class Config(BaseSettings):
    api_key: str
    base_url: str

    class Config:
        env_file = ".env"
        extra = "ignore"
