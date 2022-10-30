from content import Content


class ContentInfo:
    def __init__(self, c: Content, t_u: float, t_o: float, n: int, miss: int) -> None:
        self.c = c
        self.t_u = t_u
        self.t_o = t_o
        self.n = n
        self.miss = miss