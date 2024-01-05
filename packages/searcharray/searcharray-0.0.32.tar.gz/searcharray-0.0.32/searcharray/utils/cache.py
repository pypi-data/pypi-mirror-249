"""Shitty LRU cache implementation."""


def list_hash(lst):
    return tuple(lst)


class LRUCache:

    def __init__(self, maxsize=128):
        self.cache = {}
        self.maxsize = maxsize

    def __getitem__(self, key):
        if isinstance(key, list):
            key = list_hash(key)
        return self.cache[key]

    def __contains__(self, key):
        if isinstance(key, list):
            key = list_hash(key)
        return key in self.cache

    def __setitem__(self, key, value):
        if isinstance(key, list):
            key = list_hash(key)
        if len(self.cache) >= self.maxsize:
            self.cache.popitem()
        self.cache[key] = value

    def __len__(self):
        return len(self.cache)

    def clear(self):
        self.cache.clear()


class NoCache:

    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, key):
        raise KeyError(key)

    def __contains__(self, key):
        return False

    def __setitem__(self, key, value):
        pass

    def __len__(self):
        return 0

    def clear(self):
        self.cache.clear()
