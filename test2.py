import datetime
import time


# 这个装饰器用于改变将add函数的__doc改为原来的__doc__
def outer(src):
    def inner(dist):
        dist.__doc__ = src.__doc__
        return dist  # 如果这里不return出去，那么我在装饰wrapper的时候无法获得add这个函数对象
    return inner


# 这个装饰器用于计算add函数计算了多少秒
def count_time(fn):

    @outer(fn)# 注释掉看看add.__doc__的输出
    def wrapper(*args, **kwargs):
        """this is wrapper"""
        start = datetime.datetime.now()
        fn(*args, **kwargs)
        time.sleep(3)
        end = datetime.datetime.now()
        print((start-end).total_seconds())
        return start-end
    return wrapper


@count_time
def add(x, y):
    """this is add"""
    return x + y


add(5, 4)
print(add.__doc__)





