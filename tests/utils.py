class Any:
    def __init__(self, cls):
        self.cls = cls

    def __repr__(self):
        return f'Any({self.cls})'

    def __eq__(self, that):
        return type(that) == self.cls


class ListOf:
    def __init__(self, item, allow_empty=False):
        self.item = item
        self.allow_empty = allow_empty

    def __repr__(self):
        return f'ListOf(item={self.item}, allow_empty={self.allow_empty})'

    def __eq__(self, that):
        if type(that) != list:
            return False
        if not self.allow_empty and len(that) == 0:
            return False
        for item in that:
            if item != self.item:
                return False
        return True


class DictOf:
    def __init__(self, key, value, allow_empty=False):
        self.key = key
        self.value = value
        self.allow_empty = allow_empty

    def __repr__(self):
        return f'DictOf(key={self.key}, value={self.value}, allow_empty={self.allow_empty})'

    def __eq__(self, that):
        if type(that) != dict:
            return False
        if not self.allow_empty and len(that) == 0:
            return False
        for key, value in that.items():
            if key != self.key or value != self.value:
                return False
        return True
