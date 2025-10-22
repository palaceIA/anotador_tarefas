import redis
import json
from typing import Optional, Any
from core.settings import config


class RedisManager:
    def __init__(self, default_ttl: int = 60):
        self.host = config.REDIS_HOST
        self.port : int = config.REDIS_PORT
        self.password = config.REDIS_PASSWORD
        self.db :int = config.REDIS_DB
        self.default_ttl = default_ttl 
        self._redis_client: Optional[redis.Redis] = None
        self.connect()

    def connect(self):
            try:
                self._redis_client = redis.Redis(
                    host=self.host, 
                    port=self.port, 
                    password=self.password, 
                    db=self.db, 
                    username="default",
                    decode_responses=True
                )
                self._redis_client.ping()
                print("Redis conectado com sucesso.")
            except redis.exceptions.ConnectionError as e:
                self._redis_client = None
                print(f"Não foi possível conectar ao Redis em {self.host}:{self.port}. Caching desativado. Erro: {e}")
            except redis.exceptions.AuthenticationError:
                self._redis_client = None
                print("Erro de autenticação! Verifique se a senha do Redis está correta.")

    @property
    def client(self) -> Optional[redis.Redis]:
        return self._redis_client

    def is_connected(self) -> bool:
        return self.client is not None

    def get_cache(self, key: str) -> Optional[Any]:
        if not self.is_connected():
            return None
        
        try:
            cached_data_str = self.client.get(key)
            if cached_data_str:
                return json.loads(cached_data_str)
            return None
        except Exception as e:
            print(f"Erro ao recuperar cache da chave {key}: {e}")
            return None

    def set_cache(self, key: str, data: Any, ttl: Optional[int] = None) -> bool:
        if not self.is_connected():
            return False
        try:
            ttl = ttl if ttl is not None else self.default_ttl

            data_str = json.dumps(data)
            self.client.set(key, data_str, ex=ttl)
            return True
        except Exception as e:
            print(f"Erro ao definir cache para a chave {key}: {e}")
            return False

    def invalidate_cache(self, key: str) -> bool:
        if not self.is_connected():
            return False
        
        try:
            if isinstance(key, str):
                key = [key]
            
            deleted_count = self.client.delete(*key)
            return deleted_count > 0
        except Exception as e:
            print(f"Erro ao invalidar cache para a chave(s) {key}: {e}")
            return False
        
cache_manager = RedisManager()