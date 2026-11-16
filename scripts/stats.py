"""Small statistics helpers used by the card builder. Standard library only."""
from __future__ import annotations

import math
import random
import statistics

Z95 = 1.959963984540054


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    """Wilson score interval for a proportion k/n (95% by default)."""
    if n <= 0:
        raise ValueError("n must be positive")
    if not 0 <= k <= n:
        raise ValueError(f"k={k} outside 0..n={n}")
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def bootstrap_median_ci(values: list[float], reps: int = 2000, seed: int = 20261115) -> tuple[float, float]:
    """Percentile bootstrap 95% interval for the median, fixed seed so builds are reproducible."""
    if not values:
        raise ValueError("no values")
    rng = random.Random(seed)
    n = len(values)
    meds = sorted(statistics.median(rng.choices(values, k=n)) for _ in range(reps))
    lo = meds[int(0.025 * reps)]
    hi = meds[min(reps - 1, int(0.975 * reps))]
    return lo, hi
