from z3 import *


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
    # S = [7, 3, 2, 1, 5, 4, 8, 9, 9]
    # S = [20, 23, 25, 30, 49, 45, 27, 30, 30, 40, 22, 19]
    # S = [0, 0, 1, 1, 1, 2, 2, 2, 4, 4, 4, 5, 5, 5, 8, 8, 10, 10]
    # S = [0, 0, 1, 1, 1, 2, 3, 3, 4, 4, 4, 4, 4, 6, 6, 9, 10, 10]
    # S = [0, 0, 1, 1, 2, 2, 2, 2, 4, 4, 4, 5, 5, 5, 8, 8, 9, 10]
    S = [0, 1, 2, 5, 5, 5, 6, 6, 6, 6, 6, 8, 8, 8, 8, 9, 9, 10, 0, 0, 2, 5, 5, 5, 6, 6, 6, 6, 6, 8, 8, 8, 9, 9, 9, 10]

    solver = ThreePartition(S)
    status = solver.solve()
    if status.check() == sat:
        solution = solver.get_solution()
        print('3 partition solution:', solution)
    else:
        print('Instance of 3 partition has NO SOLUTION! => ', status.check())

