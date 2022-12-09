'''
Memory describes internal memory(IMEM), external memory(EMEM1, 2), DDR(D)
This abstraction will help a cache to easily handle memory operations.
'''

from content import Content


class Memory:
    def __init__(self, size: int) -> None:
        self.max_size = size
        self.container: list[Content] = [] # Contents inside
        pass

    def __contains__(self, c) -> bool:
        return c in self.container

    def __len__(self) -> int:
        s = [c.size for c in self.container]
        if len(s) == 0:
            return 0
        return sum([c.size for c in self.container])

    def can_add(self, size) -> bool:
        if len(self) + size <= self.max_size :
            return True
        return False

    def put(self, c: Content):
        if c in self.container:
            raise Exception("Put content Exception: Duplicated content")
        if not self.can_add(c.size):
            raise Exception("Put content Exception: Cannot add due to size")
        else:
            self.container.append(c)

    def delete(self, index: int):
        for i, c in enumerate(self.container):
            if c.index == index:
                del self.container[i]
                break

if __name__=="__main__":
    m = Memory(100)
    c1 = Content(1, 50)
    c2 = Content(2, 10)
    c3 = Content(3, 20)
    c4 = Content(4, 200)

    m.put(c1)
    m.put(c2)
    m.put(c3)
    m.delete(2)
    [print(c) for c in m.container]
    print(f'size: {len(m)}')
