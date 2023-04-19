class ClothingSet:
    def __init__(self, id, conjunto, preco):
        self.id = id
        self.conjunto = conjunto
        self.preco = preco

    def toArray(self):
        return [self.id, self.conjunto, self.preco]