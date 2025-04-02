import time
import orjson as json
import threading
from config.config import Config,get_redis_db_connection
from api.get_psu_values import get_values
from api.fake_psu_values import get_fake_values
from config.config import Config,logging

# import background task(s)

def start_background_task():
    thread = threading.Thread(target=background_task)
    thread.daemon = True  
    thread.start()

def background_task():
    try:
        r = get_redis_db_connection()
        while True:
            if Config.STORAGE_TASK:
                #check fake mode
                if Config.FAKE_VALUES:
                    r.lpush("measurements", json.dumps(get_fake_values()))  
                else:
                    if Config.LOGGING:
                        print("background_job")
                    r.lpush("measurements", json.dumps(get_values())) 
                r.ltrim("measurements", 0, Config.STORAGE_LIMIT - 1)
            time.sleep(Config.STORAGE_INTERVAL) 
    except Exception as e:
        logging.error(f"Error ({e}", exc_info=True)
        