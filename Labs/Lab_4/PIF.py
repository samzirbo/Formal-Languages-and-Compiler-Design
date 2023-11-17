class PIF(list):
    def __init__(self, array = []):
        self.__elems = array

    def append(self, elem):
        self.__elems.append(elem)

    def getElements(self):
        return self.__elems