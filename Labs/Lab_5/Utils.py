import pandas as pd
import re

class Scanner:
    def __init__(self, path, size=5):
        self.path = path
        self.__pif = PIF()
        self.__sti = SymTable(size)
        self.__stc = SymTable(size)
        self.IdFA = FA("FA/Id.txt")
        self.IntFA = FA("FA/Int.txt")

        def read_tokens(path):
            # Create list of tokens read from file but sorted by length descending
            with open(path, 'r') as f:
                list = f.read().splitlines()
                list.sort(key=len, reverse=True)
                return list  

        # Read tokens from files
        self.reserved_words = read_tokens('tokens/reserved_words.in')
        self.operators = read_tokens('tokens/operators.in')
        self.separators = read_tokens('tokens/separators.in')
    
    def isConstant(self, token):
        # int: either zero or a non-zero digit followed by zero or more digits
        # string: a sequence of characters enclosed by double quotes
        return self.IntFA.check(token) or re.match(r'^\"[a-z]+\"$', token, re.IGNORECASE)

    def isIdentifier(self, token):
        # a sequence of letters, digits, starting with a letter
        return self.IdFA.check(token)

    def tokenize(self, line):
        # Add spaces around separators
        for separator in self.separators:
            line = re.sub(rf"({re.escape(separator)})", r' \1 ', line)
        
        for operator in self.operators:
            # Add spaces around binary operators that must be surrounded by identifiers or constants
            line = re.sub(rf"([a-z0-9\"]+)\s*({re.escape(operator)})\s*([a-z0-9\"-]+)", r'\1 \2 \3', line, re.IGNORECASE)
            # Add spaces around unary operators that must be followed by an identifier or constant
            line = re.sub(rf"^\s*({re.escape(operator)})\s*([a-z0-9\"-]+)", r'\1 \2', line, re.IGNORECASE)

        return line.split()  
    
    def classify(self, token):
        if token in self.reserved_words:
            return 'res'
        elif token in self.operators:
            return 'op'
        elif token in self.separators:
            return 'sep'
        elif self.isConstant(token):
            return 'con'
        elif self.isIdentifier(token):
            return 'id'
        else:
            return 'error'  

    def scan(self):
        """
        For each line in the source file:
        1. Tokenize the line
        2. Classify each token
        3. Add the token to the PIF
        4. Add the token to the ST if it is an identifier or constant
        5. Print an error message if the token is invalid
        """
        with open(self.path, 'r') as f:
            dict = {'token':[], 'type':[]}
            lines = f.readlines()
            for i, line in enumerate(lines):
                tokens = line.split()
                tokens = self.tokenize(line)
                for token in tokens:
                    type = self.classify(token)
                    dict['token'].append(token)
                    dict['type'].append(type)
                    if type in ['id', 'con']:
                        if type == 'id':
                            pos = self.__sti.getPosition(token)
                        else:
                            pos = self.__stc.getPosition(token)
                        self.__pif.append((type, pos))
                    elif type in ['res', 'op', 'sep']:
                        self.__pif.append((token, -1))
                    else:
                        print(f"\033[91mLine {i + 1}: Lexical error: Invalid token {token}\033[0m")
                # print(f"Line {i + 1}: {tokens}")
            self.tokens = pd.DataFrame(dict)

    def save(self):
        # Save PIF and ST to files in the same directory as the source file
        source = "".join(self.path.split('.')[:-1])
        with open(source + "_PIF.out", 'w') as f:
            for token, pos in self.__pif.getElements():
                f.write(f"{token} {pos}\n")
        with open(source + "_STI.out", 'w') as f:
            f.write("Hash Table\n")
            f.write(str(self.__sti))
        with open(source + "_STC.out", 'w') as f:
            f.write("Hash Table\n")
            f.write(str(self.__stc))

    def printPIF(self):
        print('Program Internal Form:')
        print(pd.DataFrame(self.pif, columns=['token', 'pos']))
        
    def printST(self):
        print('Symbol Table (identifiers):')
        print(self.__sti)
        print('Symbol Table (constants):')
        print(self.__stc)

    def printTokens(self):
        print(self.tokens)

class FA:
    """
    Only works for deterministic finite automata (DFA)
    """
    def __init__(self, filename):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial = None
        self.final = []
        self.read(filename)

    def read(self, filename):
        with open(filename) as f:
            self.initial = f.readline().strip()
            self.final = f.readline().strip().split(',')
            for line in f:
                line = line.strip().split(',')
                if len(line[2]) > 1:
                    for letter in line[2]:
                        self.transitions[(line[0], letter)] = line[1]
                        self.alphabet.add(letter)
                else:
                    self.transitions[(line[0], line[2])] = line[1]
                    self.alphabet.add(line[2])

                self.states.add(line[0])
                self.states.add(line[1])

    def check(self, word):
        state = self.initial
        for letter in word:
            if (state, letter) in self.transitions:
                state = self.transitions[(state, letter)]
            else:
                return False
        return state in self.final

    def display(self):
        print(self)
    
    def __str__(self):
        return f"Q = {self.states}\nΣ = {self.alphabet}\nq0 = {self.initial}\nF = {self.final}\nδ = {self.transitions}"

class PIF(list):
    def __init__(self, array = []):
        self.__elems = array

    def append(self, elem):
        self.__elems.append(elem)

    def getElements(self):
        return self.__elems

class SymTable:
    def __init__(self, size):
        self.__size = size
        self.__table = HashTable(size)

    def getPosition(self, key):
        pos = self.__table.get(key)
        return pos if pos else self.__table.put(key)

    def __str__(self):
        return str(self.__table)

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
