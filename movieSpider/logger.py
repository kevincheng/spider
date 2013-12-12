import logging
import time
import sys

logger = logging.getLogger()
handler = logging.FileHandler('./log/log.txt')
logger.addHandler(handler)

def log(name, msg): 
    msg = '%s [%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), name, msg)
    sys.stdout.write(msg+'\n')
    msg = '*******************\n'+msg+'\n********************\n'
    logger.error(msg)
    

