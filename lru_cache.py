import functools

# element is params-return obj
# index 0 means the oldest record
LRUcache = []

def lru_cache(size):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            # print('%s %s():' % (size, func.__name__))
            # print('call func [{}] with args [{}] and kwargs [{}]'.format(func.__name__, args, kw))

            # cache hit
            i = 0
            while i < len(LRUcache):
                obj = LRUcache[i]
                if obj["params"] == args:
                    print ("cache hit")
                    del LRUcache[i]
                    LRUcache.append(obj)
                    return obj["return"]
                i = i+1
            
            # cache miss
            res = func(*args, **kw)
            obj = {
                "params": args,
                "return": res,
            }
            if len(LRUcache) < size:
                LRUcache.append(obj)
                return res
            else: 
                del LRUcache[0]
                LRUcache.append(obj)

            return res
        return wrapper
    return decorator


# @lru_cache(5)
# def hello(text):
#     print ("hello%s" % (text))


# if __name__ == "__main__":
#     hello("shanghai")