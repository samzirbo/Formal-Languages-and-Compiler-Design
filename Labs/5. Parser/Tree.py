import \
    json

import pandas as pd

class Tree:
    def __init__(self, start_symbol: str):
        self.ids = [0]
        self.symbols = [start_symbol]
        self.parents = [-1]
        self.right_siblings = [-1]

    def addNode(self, symbol: str, parent: int, right_sibling: int):
        self.ids.append(len(self.ids))
        self.symbols.append(symbol)
        self.parents.append(parent)
        self.right_siblings.append(right_sibling)

    def __len__(self):
        return len(self.ids)

    def __str__(self):
        df = pd.DataFrame({
            "ID": self.ids,
            "Symbol": self.symbols,
            "Parent": self.parents,
            "Right Sibling": self.right_siblings
        })
        return df.to_string(index=False)

    def save(self, filename):
        data = {
            "ID": self.ids,
            "Symbol": self.symbols,
            "Parent": self.parents,
            "Right Sibling": self.right_siblings
        }
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4, separators=(',', ': '))
                print(f">> \033[32mTree successfully saved to {filename}\033[31m")
        except Exception as e:
            print(f">> \033[31mError saving tree to {filename}\033[0m")

