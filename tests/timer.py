from datetime import datetime


def timer(func):
    def timed(*args, **kw):
        ts = datetime.now()
        print('Started:', ts.strftime("%H:%M:%S.%f"))
        result = func(*args, **kw)
        te = datetime.now()
        print('Ended:', te.strftime("%H:%M:%S.%f"))
        execution_time = te - ts
        print('Execution time:', execution_time.seconds, 'seconds')
        return result
    return timed
