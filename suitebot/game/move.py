from suitebot.game.direction import Direction


class Move:
    def __init__(self, step1: Direction, step2: Direction = None) -> None:
        if not step1:
            raise ValueError("step1 is mandatory")
        self.step1 = step1
        self.step2 = step2

    def __eq__(self, other) -> bool:
        return self.step1 == other.step1 and self.step2 == other.step2

    def __str__(self) -> str:
        if not self.step2:
            return str(self.step1)
        else:
            return str(self.step1) + str(self.step2)

    def __repr__(self):
        return "<Move: %s>" % self.__str__()
