from service.mongodb.crud.manager import TaskManager
from service.mongodb.conn.client import mongo_client
from handler.home import run_task_app

manager = TaskManager(
    db=mongo_client.get_db(),
    collection=mongo_client.get_collection()
)

if __name__=="__main__" : 
    run_task_app(manager)
