from pymongo import MongoClient
from pymongo.database import Database
from core.settings import config
from typing import Optional

class ClienteMongoDB : 
    """
        Essa classe é responsavel por lidar com o
        cliente MongoDB estabelecendo conexões e gerenciando
        o acesso ao banco de dados específico.
    """

    def __init__(self):
        self.uri = config.URI
        self._client = self.connect()
        self._db = self.get_db()

    def connect(self) -> Optional[MongoClient]: 
        """
        Estabelece e retorna a conexão com o MongoDB.
        Retorna o MongoClient ou None em caso de erro.
        """
        try : 
            print("Estabelecendo conexão com o MongoDB...")
            
            _client = MongoClient(self.uri)
            print("Conexão estabelecida com sucesso!")
            return _client
            
        except Exception as e : 
            print(f"Erro ao estabelecer conexão com o MongoDB: {e}")
            _client = None 
            return None
        
    def get_db(self) -> Database : 
        """
            Get no banco de dados definida na variavel de ambiente
        """
        db =  self._client[config.DB]
        return db
    
    def get_collection(self) : 
        """
            Get na coleção definida na variavel de ambiente
        """
        collection = self._db[config.COLLECTION]
        return collection


mongo_client = ClienteMongoDB()


