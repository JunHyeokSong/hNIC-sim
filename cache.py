import random
from content_info import ContentInfo
from content_table import ContentTable
from memory import Memory
from content import Content

SIZE_IMEM = 100
SIZE_EMEM1 = 200
SIZE_EMEM2 = 200
SIZE_DDR = 200

PERIOD_REPLACE = 10
PERIOD_SWITCH = 50

SAMPLE_SWITCH = 10

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

        self.random_fill()

    def random_fill(self):
        # fill randomly at first
        while True:
            c = (random.sample(self.contents.table.keys(), 1))[0]
            if c in self:
                continue
            if self.imem.can_add(c.size):
                self.imem.put(c)
                continue
            if self.emem1.can_add(c.size):
                self.emem1.put(c)
                continue
            if self.emem2.can_add(c.size):
                self.emem2.put(c)
                continue
            if self.ddr.can_add(c.size):
                self.ddr.put(c)
                continue
            break

    def __contains__(self, c: Content):
        return c in self.imem or c in self.emem1 or c in self.emem2 or c in self.ddr

    def query(self, c: int, time):
        c = self.contents.get_content(c)

        # Virtual time
        self.time += time
        self.contents[c].n += 1
        
        if c in self:
            self.metric["hit"] += 1
        else:
            self.metric["miss"] += 1
            self.contents[c].t_u = self.time
            self.contents[c].miss += 1

        if self.n_query % PERIOD_REPLACE:
            self.replace()
        
        if self.n_query % PERIOD_SWITCH:
            self.switch_cache()

    def replace(self):
        unoffloaded = [con for con in self.contents if not con.c in self]
        unoffloaded_sample = random.sample(unoffloaded, SAMPLE_REPLACE_UNOFF)
        unoffloaded_sample = [u for u in unoffloaded_sample if u.miss > MISS_REPLACE]

        evict = unoffloaded_sample
        for mem in [self.imem, self.emem1, self.emem2, self.ddr]:
            new_evict = []
            for e in evict:
                total_size = 0
                success = False
                evict_if_success: list[Content] = []

                priority_e = self.priority_unoffloaded(e.c)
                mem_candidates = [c for c in mem.container if self.priority_offloaded(c) < priority_e]
                mem_candidates.sort(key=lambda x: self.priority_offloaded(x), reverse=True)

                for c in mem_candidates:
                    total_size += c.size
                    evict_if_success.append(c)
                    if total_size > e.c.size:
                        success = True
                        break
                
                if success:
                    for ev in evict_if_success:
                        mem.delete(ev.index)
                        new_evict.append(ev)
                    mem.put(e)
                    e.miss = 0
                    e.t_o = self.time
                else:
                    new_evict.append(e)
            evict = new_evict

    def switch_cache(self):

        for hmem, lmem in [(self.imem, self.emem1),
                           (self.emem1, self.emem2), 
                           (self.emem2, self.ddr)]:
            hsample = random.sample(hmem.container, SAMPLE_SWITCH)
            lsample1 = random.sample(lmem.container, SAMPLE_SWITCH)
            
            hsample.sort(key=lambda x: self.priority_offloaded(x))
            lsample1.sort(key=lambda x: self.priority_offloaded(x), reverse=True)

            rev = 0
            for i in range(SAMPLE_SWITCH):
                if hsample[i] > lsample1[i]:
                    rev = i
                    break
            
            j = 0
            kick_out = []
            for i in range(rev):
                up = lsample1[i]
                while not hmem.can_add(up.size):
                    kick_out.append(hsample[j])
                    hmem.delete(hsample[j].index)
                    kick_out.append(hsample[j])
                    j += 1
                hmem.put(up)
                lmem.delete(up.index)
            
            for c in kick_out.reverse():
                if lmem.can_add(c.size):
                    lmem.put(c)

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