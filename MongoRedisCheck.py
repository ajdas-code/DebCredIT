import time
import traceback,pprint


from redis.client import Redis

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import ConnectionFailure


###########################################33
# REDIS Info
redis_host = 'redis-12495.c60.us-west-1-2.ec2.cloud.redislabs.com'
redis_port = 12495
redis_db_name = 'kitchensinkredis'
redis_db_index = 0
redis_password = 'testuser'
##############################################

#############################################
# Mongo db
mongo_host = 'mongodb+srv://testuser:testuser@kitchensink-lzcqm.mongodb.net/test?retryWrites=true&w=majority'
mongo_user = 'testuser'
mongo_db = 'kitchensink'
mongo_password = 'testuser'

#############################################
def is_redis_available(conn):
    # ... get redis connection here, or pass it in. up to you.
    try:
        conn.get(None)  # getting None returns None or throws an exception
    except (redis.exceptions.ConnectionError, 
            redis.exceptions.BusyLoadingError):
        return False
    return True

"""
host='localhost', port=6379, db=0, password=None,
                 socket_timeout=None, socket_connect_timeout=None,
                 socket_keepalive=False, socket_keepalive_options=None,
                 socket_type=0, retry_on_timeout=False, encoding='utf-8',
                 encoding_errors='strict', decode_responses=False,
                 parser_class=DefaultParser, socket_read_size=65536,
                 health_check_interval=0, client_name=None, username=None
"""

print('connecting to redis "{}"'.format(redis_host))
time.sleep(5)
conn_pool = Redis(host=redis_host,port=redis_port,db=redis_db_index ,password=redis_password)
pprint.pprint(conn_pool.__dict__)
try:
    data = conn_pool.ping()
    print('Successfully connected to redis...{0}'.format(data))
except:
    print('Redis connection error')
    # handle exception
    traceback.print_stack()

print(".......redis check done..........")

########################################################################    
print('connecting to mongo "{}"'.format(mongo_host))
time.sleep(5)
client = MongoClient(mongo_host, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
pprint.pprint(client.__dict__)
try:
    info = client.server_info() # Forces a call.
    info1= client.admin.command('ismaster')
    print('Successfully connected to Mongo...{0}'.format(info))
except ServerSelectionTimeoutError:
    print("Mongo server is down.")
except ConnectionFailure:
   print("Mongo Server not available")
except:
    traceback.print_stack()
    print(err)

print(".......Mongo check done..........")
