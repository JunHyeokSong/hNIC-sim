import numpy as np

# Zipf distribution -> [0, mod) : frequency of access: 1 > 2 > 3 > ... > mod-1 > 0
def zipf(alpha, mod, size) -> list:
    return np.random.zipf(alpha, size) % mod

# Random wating time in poisson process
def random_wating(lam):
    return -np.log(1.0 - np.random.random()) / lam

if __name__=="__main__":
    print(zipf(1.5, 10, 100))