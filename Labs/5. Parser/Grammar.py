import pandas as pd
import json

class Grammar:
    def __init__(self, path: str):
        self.nonterminals = []
        self.terminals = []
        self.productions = {}
        self.start = None

        with open(path, 'r') as file:
            try:
                data = json.load(file)
                self.nonterminals = data['NonTerminals']
                self.terminals = data['Terminals']
                self.productions = data['Productions']
                self.start = data['Start']
                self.setProductionNo()
            except Exception as e:
                print(e)
                print("Invalid JSON file")
                return

        print('Nonterminals:', self.nonterminals)
        print('Terminals:', self.terminals)
        print('Start:', self.start)
        self.getProductions()

    def getProduction(self, nonterminal: str):
        return self.productions[nonterminal]

    def isCFG(self):
        """
        A grammar is called Context-Free Grammar (CFG) if:
        1. Starting symbol is in the set of productions
        2. All left-hand sides of productions are nonterminals
        3. All right-hand sides of productions are strings of terminals and nonterminals (including ε)
        """
        if self.start not in self.nonterminals or self.start not in self.productions:
            return False

        for nonterminal, productions in self.productions.items():
            if nonterminal not in self.nonterminals:
                raise Exception(f"Invalid nonterminal: {nonterminal}")
                return False

            for production in productions:
                for symbol in production:
                    if not (symbol in self.nonterminals or symbol in self.terminals or symbol == 'ε'):
                        raise Exception(f"Invalid symbol: {symbol}")
                        return False
        return True

    def getProductions(self):
        print("Productions:")
        for nonterminal, productions in self.productions.items():
            production_str = f"  {nonterminal} -> {' | '.join(' '.join(prod) for prod in productions)}"
            print(production_str)

    def getProductionsAsList(self):
        print("Productions:")
        for nonterminal, productions in self.productions.items():
            for production in productions:
                production_str = f" [{self.productionNo[(nonterminal, ''.join(production))]}] {nonterminal} -> {' '.join(production)}"
                print(production_str)

    def setProductionNo(self):
        i = 1
        self.productionNo = {}
        for nonterminal, productions_list in self.productions.items():
            for production in productions_list:
                key = (nonterminal, "".join(production))
                self.productionNo[key] = i
                i += 1