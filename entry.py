# Entry point

from simulator import Simulator
import tools
from itertools import product
from tqdm import tqdm

N_CONTENTS = 1000
WARMUP = 10000
N_REQUESTS = 50000

ALPHA = 1.5
LAMBDA = 100    # Requests per second

requests = tools.zipf(ALPHA, N_CONTENTS, WARMUP + N_REQUESTS)
print(f'Requests: {requests}')
# Simulation scenario
requests = [(r, tools.random_wating(LAMBDA)) for r in requests]

upToFive = [1, 2, 3]

items = list(product(upToFive, upToFive, upToFive))
items1 = [(i, j, k) for i, j, k in items if i > j]
items2 = [(i, j, k) for i, j, k in items if i > j]

parameters = {}
saved_parameter = None
best = -1
for a, b, c in tqdm(items1, desc="offloading: "):
    for x, y, z in tqdm(items2, desc="unoffloading: "):
        parameters["alpha"] = a
        parameters["beta"] = b
        parameters["gamma"] = c

        parameters["kappa"] = x
        parameters["mu"] = y
        parameters["lam"] = z

        scenario = requests
        n_contents = N_CONTENTS

        simulator = Simulator(scenario, parameters, n_contents)
        simulator.execute()
        print(f'\nhit ratio: {simulator.score()} with parameter: {parameters}\n')
        if simulator.score() > best:
            best = simulator.score()
            saved_parameter = parameters

print(f'Best hit ratio: {best}')
print(f'From parameters: {saved_parameter}')


        