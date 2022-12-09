# Content, only has size.

class Content:
    def __init__(self, index: int, size: int) -> None:
        self.index = index
        self.size = size
    
    def __str__(self):
        return f'Content(index: {self.index}, size: {self.size})'

    def __hash__(self):
        return self.index

def contentSizePolicy(i):
    return 10 + (i//100) 