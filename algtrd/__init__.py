from algtrd.iov import *
from algtrd.strategy import *
from algtrd.storage import *
import os

global storage_name
storage_name = 'parameters.json'

if not os.path.exists(storage_name):
    with open(storage_name, 'w') as create: pass

