from HashTable import HashTable

class SymTable:
    def __init__(self, size):
        self.__size = size
        self.__table = HashTable(size)

    def getPosition(self, key):
        pos = self.__table.get(key)
        return pos if pos else self.__table.put(key)

    def __str__(self):
        return str(self.__table)