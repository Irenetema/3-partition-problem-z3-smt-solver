import random
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

from z3 import *


def generate_test_set(values_range=None, size_of_set=21, is_sat=True):
    if values_range is None:
        values_range = [0, 100]

    if size_of_set % 3 != 0:
        raise ValueError('The size of the set should be divisible by 3!')

    final_set = []
    if is_sat:
        range_length = values_range[1] + values_range[0]
        target_nbr = random.randint(int(range_length / 2), values_range[1])

        while len(final_set) < size_of_set:
            subset = []
            subset_elt1 = random.randint(values_range[0], int(range_length/3))
            subset.append(subset_elt1)

            upper_bound = target_nbr - subset_elt1
            subset_elt2 = random.randint(values_range[0], upper_bound - 2)
            while subset_elt1 + subset_elt2 >= target_nbr:
                print(f'In while loop: Elt1: {subset_elt1};   Elt2: {subset_elt2};   Target: {target_nbr}')
                # subset_elt2 = random.randint(values_range[0], target_nbr - 2)
                subset_elt2 = random.randint(values_range[0], upper_bound - 2)
            subset.append(subset_elt2)

            subset_elt3 = target_nbr - (subset_elt1 + subset_elt2)
            if subset_elt3 <= 0:
                raise ValueError('The elements of the subset don\'t add to the target value!')
            subset.append(subset_elt3)

            final_set = final_set + subset
    else:
        while len(final_set) < size_of_set:
            subset = []
            subset_elt1 = random.randint(values_range[0], values_range[1])
            subset.append(subset_elt1)

            subset_elt2 = random.randint(values_range[0], values_range[1])
            subset.append(subset_elt2)

            subset_elt3 = random.randint(values_range[0], values_range[1])
            subset.append(subset_elt3)

            final_set = final_set + subset
    return final_set


class ThreePartition:
    def __init__(self, input_set):
        self.input_set = input_set
        self.solution = None

    def solve(self):
        N = len(self.input_set)
        n_part = int(N / 3)
        if N % 3 != 0 or N < 3:
            print('No solution!')
            return False

        target_nber = sum(self.input_set) / n_part
        s = Solver()

        # declare variables for each row and column of the matrix
        # matrix = [[Int("{}{}".format(r, c)) for c in range(n_part)] for r in range(N)]
        matrix = [[Bool("X_{}_{}".format(r, c)) for c in range(N)] for r in range(n_part)]

        # Add constraints that there are exactly 3 true per row
        for r in range(n_part):
            s.add(Sum([If(Bool("X_{}_{}".format(r, c)), 1, 0) for c in range(N)]) == 3)

        # Add constraints that there are exactly 1 true per column
        for c in range(N):
            s.add(Sum([If(Bool("X_{}_{}".format(r, c)), 1, 0) for r in range(n_part)]) == 1)

        # Add constraints that the some of elements that are true per row equals the target number
        for r in range(n_part):
            s.add(Sum([If(Bool("X_{}_{}".format(r, c)), self.input_set[c], 0) for c in range(N)]) == target_nber)

        if s.check() == sat:
            self.solution = s
        return s

    def get_solution(self):
        if self.solution.check() is None:
            raise ValueError('That input has no solution or has not been solved yet!')

        N = len(self.input_set)
        n_part = int(N / 3)
        found_solution = []
        for r in range(n_part):
            row_part = []
            for c in range(N):
                if is_true(self.solution.model().eval(Bool("X_{}_{}".format(r, c)))):
                    row_part.append(self.input_set[c])
            found_solution.append(row_part)
            # found_solution.append([If(Bool("X_{}{}".format(r, c)), self.input_set[c], 0) for c in range(N)])

        return found_solution


if __name__ == '__main__':
    ## S = [7, 3, 2, 1, 5, 4, 8, 9, 9]
    ## S = [20, 23, 25, 30, 49, 45, 27, 30, 30, 40, 22, 19]
    all_runtime = []

    # set_sizes = [6, 12, 24, 36, 48, 51]
    set_sizes = [6, 12, 24, 27, 30, 36, 42, 51, 60, 69]
    values_ranges = [[1000, 5000], [100000, 500000], [100000000, 500000000], [10000000000, 50000000000]]

    for v_range in tqdm(values_ranges):
        all_runtime = []
        for s in tqdm(set_sizes):
            S = generate_test_set(
                values_range=v_range,
                size_of_set=s,
                is_sat=True  # defines if the set generated should be a satisfiable instance
            )
            # print('-----> Set generated: ', S)
            print('-----> Size of set generated: ', len(S))

            time_start = time.time()
            solver = ThreePartition(S)
            status = solver.solve()
            if status.check() == sat:
                solution = solver.get_solution()
                print('3 partition solution:', solution)
            else:
                print('Instance of 3 partition has NO SOLUTION! => ', status.check())
            time_end = time.time()
            runtime = time_end - time_start
            all_runtime.append(runtime)
            print('Size {} --> solved in {:.2f}s'.format(s, time_end - time_start))

        plt.plot(set_sizes, all_runtime, '.-', label=f'values: {v_range}')
    plt.xlabel('Size of input set (S)')
    plt.ylabel('Running time (second)')
    plt.title('Performance on satisfiable instances')
    plt.legend()
    plt.show()

    # print(solver.solution)
    # print(solver.check())
    # print(solver.solution.model())
    #
    # # m = solver.solution.model()
    # # print(solver.solution.statistics())
    # # if is_true(m.eval(Bool('X_0_2'))):
    # #     print('Yes it is true!')
