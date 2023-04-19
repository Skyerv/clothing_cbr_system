class ClothingSet:
    def __init__(self, conjunto, preco):
        self.conjunto = conjunto
        self.preco = preco

    def toArray(self):
        return [self.conjunto, self.preco]