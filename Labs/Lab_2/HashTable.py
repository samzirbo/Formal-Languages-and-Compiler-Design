class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        total = 0
        for c in str(key):
            total += ord(c)
        return total % self.size

    def put(self, key):
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = [key]
            return index, 0
        else:
            if key not in self.table[index]:
                self.table[index].append(key)
                return index, len(self.table[index]) - 1
            return False

    def get(self, key):
        index = self._hash(key)
        if self.table[index] is not None and key in self.table[index]:
            return index, self.table[index].index(key)
        return None
    
    def getByPos(self, pos):
        if self.table[pos[0]] is not None and len(self.table[pos[0]]) > pos[1]:
            return self.table[pos[0]][pos[1]]
        return None

    def remove(self, key):
        index = self._hash(key)
        if self.table[index] and key in self.table[index]:
            self.table[index].remove(key)
        else:
            raise KeyError(f"Key not found: {key}")
    
    def __str__(self):
        table_str = ""
        for i in range(self.size):
            if self.table[i] is not None:
                for j in range(len(self.table[i])):
                    table_str += f"({i}, {j}) {self.table[i][j]}\n"
        return table_str
    
    def getSize(self):
        return self.size
