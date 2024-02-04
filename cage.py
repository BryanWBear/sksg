class Cage:
    def __init__(self, initial_tile) -> None:
        self.tiles = [initial_tile]

    def merge(self, other):
        self.tiles = self.tiles + other.tiles

    