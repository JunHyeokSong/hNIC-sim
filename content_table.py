from typing import Dict
from content import Content
from content_info import ContentInfo


class ContentTable:
    def __init__(self) -> None:
        self.table: Dict[Content, ContentInfo] = {}
        pass

    def add(self, c: Content, t_u: float, t_o: float, n: int, miss: int):
        self.table[c] = ContentInfo(c, t_u, t_o, n, miss)

    def __getitem__(self, c: Content):
        return self.table[c]

    def get_content(self, idx: int):
        for k in self.table.keys():
            if k.index == idx:
                return k
