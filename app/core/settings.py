import os 

from pydantic_settings import BaseSettings

class Settings(BaseSettings): 
    """
        Essa classe herda da classe mãe BaseSettings
        para gerenciarmos acesso as variaveis de ambiente
        de forma segura
    """
    DB : str = os.getenv("DB")
    URI : str = os.getenv("URI")
    COLLECTION : str = os.getenv("COLLECTION")

    REDIS_HOST : str = os.getenv("REDIS_HOST")
    REDIS_PORT : int = os.getenv("REDIS_PORT")
    REDIS_PASSWORD : str = os.getenv("REDIS_PASSWORD")
    REDIS_DB : int = os.getenv("REDIS_DB")

    class Config:
        env_file = ".env"


config = Settings()