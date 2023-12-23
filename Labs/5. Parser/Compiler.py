from Grammar import Grammar
from Utils import Scanner
from Parser import Parser

class Compiler:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.parser = Parser(grammar)

    def compile(self, source=None, pif=None):
        if source:
            scanner = Scanner(source)
            output, content = scanner.scan()
            scanner.save()
            # print(output, content)
            if output == "Errors":
                for error in content:
                    print(f"\033[31mLexical error: {error}\033[0m")
            else:
                print(f"Tokens: {content}")
                self.parser.parse(content)
        else:
            with open(pif) as f:
                tokens = [line.split()[0] for line in f.readlines()]
                self.parser.parse(tokens)


if __name__ == "__main__":
    g1 = Grammar('Grammars/g2.json')
    compiler = Compiler(g1)
    compiler.compile(source='IO/p1.txt')

