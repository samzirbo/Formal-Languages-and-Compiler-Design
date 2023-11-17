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
        # path = []
        state = self.initial
        for letter in word:
            if (state, letter) in self.transitions:
                # path.append((state, letter, self.transitions[(state, letter)]))
                state = self.transitions[(state, letter)]
            else:
                return False
        # for transition in path:
        #     print(f"δ({transition[0]}, {transition[1]}) = {transition[2]}")
        return state in self.final

    def display(self):
        print(self)
    
    def __str__(self):
        return f"Q = {self.states}\nΣ = {self.alphabet}\nq0 = {self.initial}\nF = {self.final}\nδ = {self.transitions}"
    
if __name__ == '__main__':
    fa = FA('FA/Id.txt')
    # fa.display()
    print(fa.check('aabb'))
    print(fa.check('s4f'))
    print(fa.check('4affdex'))