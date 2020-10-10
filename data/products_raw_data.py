import numpy as np
import math as m

PARAMS_RANGES = \
    [
        {
            "p1": np.arange(-1., 1., 0.1),
            "p2": np.arange(1, 3, 1),
            "p3": (1, 2, 50, 200),
            "p4": np.arange(100, 1000, 1),
            "p5": (2.3, 2.7, 3.5)
        },
        {
            "p1": np.arange(0.1, 1., 0.2),
            "p2": ("A", "A+", "AA", "AA+", "B"),
            "p3": [i ** 2 for i in range(12)],
            "p4": [0, 1],
            "p5": [0, 1],
            "p6": [0, 1],
            "p7": [0, 1],
        }
    ]

PARAMS_COST_WEIGHTS = \
    [
        [
            [-i ** 2 for i in PARAMS_RANGES[0]["p1"]],
            (0.2, 0.45, 0.35),
            (0.1, 0.2, 0.5, 0.2),
            np.arange(1, len(PARAMS_RANGES[0]["p4"])),
            (0.9, 0.01, 0.09)
        ],
        [
            [i ** 4 for i in PARAMS_RANGES[1]["p1"]],
            [10, 13, 24, 240, 57],
            [(i + 0.1) ** 2 / (i+0.2) ** 1.9 for i in range(12)],
            [0.01, 0.99],
            [0.4, 0.6],
            [0.7, 0.3],
            [0.5, 0.5]
        ]
    ]

COST_MULTIPLIERS = [10, 1.2]
STOCHASTIC_WEIGHTS = [1,2.5]
