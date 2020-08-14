class Moves:
    def __init__(self, fast_moves: list = None, charge_moves: list = None):
        self.fast_moves = None if fast_moves is None else [move.replace("_FAST", "").replace("_", " ") + "\n" for move in fast_moves]
        self.charge_moves = None if charge_moves is None else [move.replace("_", " ") + "\n" for move in charge_moves]

    def __str__(self):
        return f"Fast moves: {self.fast_moves}, charge moves: {self.charge_moves}"
