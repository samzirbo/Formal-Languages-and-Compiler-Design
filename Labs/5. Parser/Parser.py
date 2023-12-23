from Grammar import Grammar
import pandas as pd
from collections import deque
from Tree import Tree

class Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = None
        self.tree = None
        self.first = {}
        self.follow = {}

    def isFinal(self, symbol: str):
        """
        Check if the first of the symbol can be currently computed
        """
        for production in self.grammar.getProduction(symbol):
            for element in production:
                if element in self.grammar.terminals:
                    break
                if not self.first[element] and element != symbol:
                    return False
        return True

    def First(self):
        """
        Computes the first of all the nonterminals
        """
        # initialize the first of all nonterminals with empty sets
        for nonterminal in self.grammar.nonterminals:
            self.first[nonterminal] = set()

        # initialize the first of all terminals
        for terminal in self.grammar.terminals + ['ε']:
            self.first[terminal] = {terminal}

        # loop until all the nonterminals are in their final form
        while not all(i for i in self.first.values()):
            for nonterminal in self.grammar.nonterminals:
                # if the first can be computed
                if self.isFinal(nonterminal) and not self.first[nonterminal]:
                    for production in self.grammar.getProduction(nonterminal):
                        first_prod = self.getFirst(production)
                        self.first[nonterminal].update(first_prod)

        self.printFirst()


    def getFirst(self, symbols: list):
        """
        Computes the string concatenation of length 1 of the first of the symbols
        """
        result = set()
        for idx, symbol in enumerate(symbols):
            result.update(self.first[symbol].difference({'ε'})) # we add the first of the symbol without ε
            if 'ε' not in self.first[symbol]: # if the first of the symbol doesn't contain ε we stop
                break
            elif idx == len(symbols) - 1: # if all the symbols have ε in their first
                result.add('ε')

        return result

    def Follow(self):
        """
        Computes the follow of all the nonterminals
        """
        # initialize the first of all nonterminals with empty sets
        for nonterminal in self.grammar.nonterminals:
            self.follow[nonterminal] = set()
        self.follow[self.grammar.start].add("$")

        modified = True
        while modified:
            modified = False
            for nonterminal in self.grammar.nonterminals:
                # iterate over the prod that have nonterminal as rhs
                for lhs, productions in self.grammar.productions.items():
                    for rhs in [prod for prod in productions if nonterminal in prod]:

                        indices = [i for i, x in enumerate(rhs) if x == nonterminal] # get all the indices of the nonterminal in the rhs
                        for idx in indices:

                            if idx == len(rhs) - 1: # case A -> aB
                                modified = not self.follow[lhs].issubset(self.follow[nonterminal]) # check if the follow of lhs is a subset of the follow of nonterminal
                                self.follow[nonterminal].update(self.follow[lhs])

                            else: # case A -> aBb
                                if 'ε' in self.getFirst(rhs[idx+1:]): # if the first of the rest of the rhs contains ε, we add the follow of lhs
                                    modified = not self.follow[lhs].issubset(self.follow[nonterminal])
                                    self.follow[nonterminal].update(self.follow[lhs])

                                self.follow[nonterminal].update(self.getFirst(rhs[idx+1:]).difference({'ε'}))
        self.printFollow()

    def buildTable(self):
        """
        Computes the First and Follow of the grammar and builds the parsing table
        """
        self.First()
        self.Follow()

        # initialize the parsing table
        self.table = dict()
        for row in self.grammar.nonterminals + self.grammar.terminals + ['$']:
            self.table[row] = dict()
            for column in self.grammar.terminals + ['$']:
                self.table[row][column] = '-'

        for terminal in self.grammar.terminals:
            self.table[terminal][terminal] = 'pop'
        self.table['$']['$'] = 'acc'

        # iterate over all the productions
        for lhs in  self.grammar.nonterminals:
            for rhs in self.grammar.getProduction(lhs):
                for first in self.getFirst(rhs):
                    if first == 'ε': # case A -> ε
                        for follow in self.follow[lhs]:
                            if self.table[lhs][follow] != '-':
                                print(f">> \033[31mConflict: [{lhs}, {follow}]: {self.table[lhs][follow]} and {self.getPair(lhs, rhs)}\033[0m")
                            else:
                                self.table[lhs][follow] = self.getPair(lhs, rhs) # add the production to the follow of lhs
                    else: # case A -> sequence
                        if self.table[lhs][first] != '-':
                                print(f">> \033[31mConflict: [{lhs}, {first}]: {self.table[lhs][first]} and {self.getPair(lhs, rhs)}\033[0m")
                        else:
                            self.table[lhs][first] = self.getPair(lhs, rhs) # add the production to the first of lhs

        self.printTable()

    def parse(self, sequence: list):
        """
        Build the parsing table and parse the sequence
        Output:
            the production used to parse the sequence
            the derivation of the sequence
            the tree of the sequence
        """
        for symbol in sequence:
            if symbol not in self.grammar.terminals:
                print(f">> \033[31mSymbol {symbol} is not in the grammar\033[0m")
                return

        self.buildTable()

        # initialize the input and the work stack
        input = deque(sequence + ["$"])
        work = deque([self.grammar.start] + ["$"])

        productions = []
        derivations = [" ".join(list(work))]
        ids = deque([0]) # ids of the nodes in the tree
        self.tree = Tree(self.grammar.start)

        while True:

            action = self.table[work[0]][input[0]]
            if action == 'acc' or action == '-':
                break
            elif action == "pop":
                work.popleft()
                input.popleft()
                ids.popleft()

                derivations.append(" ".join(list(work)))
            else:
                work.popleft()
                parent = ids.popleft() # take the leftmost id which represents the parent of the production

                production, productionNo = action
                productions.append(productionNo)

                for idx, element in enumerate(reversed(production)): # add the production to the work stack in reverse order
                    if element != 'ε':
                        work.appendleft(element)
                        ids.appendleft(len(self.tree) + len(production) - 1 - idx) # add the id of the node to the ids stack

                for idx, element in enumerate(production): # add the production to the tree
                    if element != 'ε':
                        self.tree.addNode(element, parent, -1 if idx == len(production) - 1 else len(self.tree) + 1)

                derivations.append(" ".join(list(work)))

        print(f"{productions=}")
        print(f"{derivations=}")
        print(f"tree: \n {self.tree}")

        if action == 'acc':
            print(">> \033[32mSequence accepted\033[0m")
        else:
            print(f">> \033[31mSyntax error: {input[0]}\033[0m")
            print(">> \033[31mSequence rejected\033[0m")

    def saveTree(self, filename):
        if self.tree:
            self.tree.save(filename)
        else:
            print(">> \033[31mNo tree to save\033[0m")

    def printFollow(self):
        print("Follow:")
        for nonterminal in self.grammar.nonterminals:
            print(f"   {nonterminal} -> {self.follow[nonterminal]}")
    def printFirst(self):
        print("First:")
        for nonterminal in self.grammar.nonterminals:
            print(f"   {nonterminal} -> {self.first[nonterminal]}")
    def printTable(self):
        print("Table:")
        print(pd.DataFrame(self.table).T)

    def getPair(self, nonterminal, production):
        """
        Returns the pair (production, productionNo) to be added to the parsing table
        """
        return production, self.grammar.productionNo[(nonterminal, ''.join(production))]

if __name__ == '__main__':
    # g1 = Grammar('Grammars/g1.json')
    # parser = Parser(g1)
    # parser.parse(["a", "*", "(", "a", "+", "a", ")"])

    g2 = Grammar('Grammars/g2.json')

    with open('IO/p1_PIF.out') as f:
        sequence = [line.split()[0] for line in f.readlines()]
    # for symbol in sequence: if if id make it ID and if con make it CONST
    for idx, symbol in enumerate(sequence):
        if symbol == 'id':
            sequence[idx] = 'ID'
        elif symbol == 'con':
            sequence[idx] = 'CONST'

    parser = Parser(g2)
    parser.parse(sequence)

    # g = Grammar('Grammars/conflict.json')
    # parser = Parser(g)
    # parser.parse(["a", "b"])
