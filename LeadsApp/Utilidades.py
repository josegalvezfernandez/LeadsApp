
from datetime import datetime, date
import numpy as np

def datetime64_to_date(datetime64):
    ts = ((datetime64 - np.datetime64("1970-01-01T00:00:00Z")) / np.timedelta64(1, "s"))  # timestamp
    return datetime.utcfromtimestamp(ts).date()


def date_to_datime64(dt):
    dtime = datetime.combine(dt, datetime.min.time())
    # print(dtime)#Todos los print hacen de debbuger ¿No funciona?
    return np.datetime64(dtime)