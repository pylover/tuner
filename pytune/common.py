def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class Event(object):
    
    def __init__(self):
        self.handlers = []
    
    def add(self, handler):
        self.handlers.append(handler)
        return self
    
    def remove(self, handler):
        self.handlers.remove(handler)
        return self
    
    def fire(self, *args,**kwargs):
        for handler in self.handlers:
            handler(*args,**kwargs)
    
    __iadd__ = bind = add
    __isub__ = unbind = remove
    __call__ = fire