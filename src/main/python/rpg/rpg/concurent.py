from functools import wraps
from multiprocessing import Lock

def synchonized(member):
    @wraps(member)
    def wrapper(*args, **kwargs):
        lock = vars(member).get("_synchronized_lock", None)
        result: str = ""
        try:
            if (lock is None):
                lock = vars(member).setdefault("_synchronized_lock", Lock())
            lock.acquire()
            result = member(*args, **kwargs)
            lock.release()
        except Exception as error:
            lock.release()
            raise error
        return result
    return wrapper