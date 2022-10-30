import random
from content_info import ContentInfo
from content_table import ContentTable
from memory import Memory
from content import Content

SIZE_IMEM = 1000
SIZE_EMEM1 = 5000
SIZE_EMEM2 = 5000
SIZE_DDR = 20000

PERIOD_REPLACE = 10
PERIOD_SWITCH = 50

EPSILON = 0.000001
OMEGA = 1.0

SAMPLE_REPLACE_UNOFF = 10
MISS_REPLACE = 3

class Cache:
    def __init__(self, contents: ContentTable, parameters) -> None:
        self.contents = contents
        self.parameters = parameters

        self.metric = {}
        self.metric["hit"] = 0
        self.metric["miss"] = 0

        self.imem = Memory(SIZE_IMEM)
        self.emem1 = Memory(SIZE_EMEM1)
        self.emem2 = Memory(SIZE_EMEM2)
        self.ddr = Memory(SIZE_DDR)

        self.time = 0.0    # Virtual time
        self.n_query = 0   # Number of query

    def random_fill(self):
        pass

    def __contains__(self, c: Content):
        return c in self.imem or c in self.emem1 or c in self.emem2 or c in self.ddr

    def query(self, c: Content, time):
        # Virtual time
        self.time += time
        self.contents[c].n += 1
        
        if c in self:
            self.metric["hit"] += 1
        else: 
            self.metric["miss"] += 1
            self.contents[c].t_u = self.time
            self.contents[c].miss += 1

    def replace(self):
        unoffloaded = [con for con in self.contents if con.c in self]
        unoffloaded_sample = random.sample(unoffloaded, SAMPLE_REPLACE_UNOFF)
        unoffloaded_sample = [u for u in unoffloaded_sample if u.miss > MISS_REPLACE]
        
        for u in unoffloaded_sample:
            priority_u = self.priority_unoffloaded(u.c)
            imem_candidates = [c for c in self.imem.container if self.priority_offloaded(c) < priority_u]
            if len(imem_candidates) != 0:
                total = 0
                evict = []
                success = False
                imem_candidates.sort(key=lambda x: self.priority_offloaded(x))
                for c in imem_candidates:
                    total += c.size
                    evict.append(c)
                    if total > u.c.size:
                        success = True
                        break
                if success:
                    for e in evict:
                        self.imem.delete(e.index)
                    self.imem.put(u.c)
                
    def replace_from(self, u: ContentInfo, mem: Memory):
        priority_u = self.priority_unoffloaded(u.c)
        mem_candidates = [c for c in mem.container if self.priority_offloaded(c) < priority_u]
        if len(mem_candidates) != 0:
            total = 0
            evict = []
            success = False
            mem_candidates.sort(key=lambda x: self.priority_offloaded(x))
            for c in mem_candidates:
                total += c.size
                evict.append(c)
                if total > u.c.size:
                    success = True
                    break
            if success:
                for e in evict:
                    mem.delete(e.index)
                self.evicts
                self.imem.put(u.c)
                u.miss = 0
                u.t_o = self.time

    def evicts(self, evict, lower):
        if len(lower) == 0:
            return
        
        pass

    def switch_cache(self):
        pass

    def priority_offloaded(self, content: Content):
        alpha = self.parameters["alpha"]
        beta = self.parameters["beta"]
        gamma = self.parameters["gamma"]
        t = self.contents[content]
        return (t.n ** beta) / ((content.size ** alpha) * (self.time - t.t_o) ** gamma + EPSILON) 

    def priority_unoffloaded(self, content: Content):
        kappa = self.parameters["kappa"]
        mu = self.parameters["mu"]
        lam = self.parameters["lam"]
        t = self.contents[content]
        return (t.n ** mu) / ((content.size ** kappa) * (self.time - t.t_u) ** lam + EPSILON)