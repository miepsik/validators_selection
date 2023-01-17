class Cache:
    def __init__(self):
        self.cache = {}

    def __history2tuple(self, history):
        return tuple([(tuple(a), tuple(b)) for (a, b) in history])

    def __history2str(self, history):
        return str([[list(a), list(b)] for (a,b) in history])

    def query(self, history):   
        if not isinstance(history, str):
            key = self.__history2str(history)
        else:
            key = history
        if key in self.cache:
            return self.cache[key]
        else:
            return None

    def add(self, history, proposition):
        if not isinstance(history, str):
            key = self.__history2str(history)
        else:
            key = history
        self.cache[key] = proposition
