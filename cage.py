class Cage:
    def __init__(self, initial_tile) -> None:
        self.tiles = [initial_tile]

    def merge(self, other):
        self.tiles = list(set(self.tiles + other.tiles))  # not sure if this is necessary, but just in case.


    