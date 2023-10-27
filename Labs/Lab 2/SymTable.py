from HashTable import HashTable

class SymTable:
    def __init__(self, size):
        self.size = size
        self.__table = HashTable(size)

    def getTable(self):
        return self.__table

    def getPosition(self, key):
        pos = self.__table.get(key)
        return pos if pos else self.__table.put(key)

    def __str__(self):
        return str(self.__table)


if __name__ == '__main__':
    # Example usage
    """
    a: int
    b: int
    c: int
    a = 1
    b = 2
    c = a + b
    << "c=" + c
    """
    st = SymbolTable(5)
    print(st.getPosition("a"))
    st.getPosition("a")
    st.getPosition("b")
    st.getPosition("c")
    st.getPosition("1")
    st.getPosition("2")
    st.getPosition("c=")
    print(st)