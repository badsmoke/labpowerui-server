import os
import redis
import sys
#power supply
from owon_psu import OwonPSU
import logging

logging.basicConfig(
    level=logging.ERROR, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)



class Config:
    #redis
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    #save defaults
    STORAGE_TASK=os.getenv("FAKE_VALUES", "true").lower() in ("true", "1", "yes")
    STORAGE_INTERVAL=float(os.getenv("STORAGE_INTERVAL",1))
    STORAGE_LIMIT=int(os.getenv("STORAGE_LIMIT",1000))
    #fake values
    FAKE_VALUES=os.getenv("FAKE_VALUES", "False").lower() in ("true", "1", "yes")
    LOGGING=os.getenv("FAKE_VALUES", "False").lower() in ("true", "1", "yes")
    #USB
    USB_DEVICE=os.getenv("USB_DEVICE","/dev/ttyUSB0")
    if os.path.exists(USB_DEVICE):
        try:
            USB_DEVICE_OBJECT=OwonPSU(USB_DEVICE)
            USB_DEVICE_OBJECT.open()
            print("Devices opened.")
        except Exception as e:
            print(f"Device could not be opened: {e}")
            USB_DEVICE_OBJECT = None
    else:
        print(f"warning: Device {USB_DEVICE} does not exist, or no permission.")
        USB_DEVICE_OBJECT = None



def get_redis_db_connection():

    try:
        return redis.Redis(
            host=Config.REDIS_HOST, 
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB, 
            decode_responses=True
        )
    except Exception as e:
        logging.error(f"Error ({e}", exc_info=True)
        raise


