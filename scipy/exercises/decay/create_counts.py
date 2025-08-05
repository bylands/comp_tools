import numpy as np

rng = np.random.default_rng()
low = 1
high = 826_134
n_dice = 10_000_000
n_trials = 2_500


def get_counts():
    simulation = rng.integers(low=low, high=high, size=n_dice)
    return np.sum(simulation == 1)


counts = [int(get_counts()) for _ in range(n_trials)]
np.savetxt("counts.csv", counts, delimiter=",")
