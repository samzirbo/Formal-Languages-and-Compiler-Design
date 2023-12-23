from HashTable import HashTable

class SymTable:
    def __init__(self, size):
        self.size = size
        self.table = HashTable(size)

    def getPosition(self, key):
        pos = self.table.get(key)
        return pos if pos else self.table.put(key)

    def __str__(self):
        return str(self.table)