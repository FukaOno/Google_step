#!/usr/bin/env python3

from common import format_tour, read_input

import solver_not_random

CHALLENGES = 7


def generate_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        for solver, name in [(solver_not_random, 'not_random')]:
            tour = solver.solve(cities)
            with open(f'output_{i}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')


if __name__ == '__main__':
    generate_output()
