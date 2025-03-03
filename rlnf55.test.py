"""Test file for rlnf55.py
"""


from timeit import default_timer as timer
from rlnf55 import load_dimacs, unit_propagate, simple_sat_solve


class Test:
    """Class for running tests
    """
    def __init__(self, func, args: list, output):
        self.func = func
        self.args = args
        self.output = output
        print()

    def run(self) -> None:
        """Runs the function using the provided arguments and compares result with expected output
        """
        print(f"Testing function {self.func.__name__}")
        try:
            result = self.func(*self.args)
            assert result == self.output
            print("    Function works")
        except AssertionError:
            print("    Function does not work")

    def time(self) -> None:
        """Measures time taken for a function to run 1000 times
        """
        print(f"Timing function {self.func.__name__}")
        start = timer()
        for _ in range(1000):
            __ = self.func(*self.args)
        end = timer()
        time_elapsed = end - start
        print(f"    Function took {time_elapsed}s")


if __name__ == "__main__":
    # Test `load_dimacs` function
    test = Test(load_dimacs, ["Examples/sat.txt"], [[1], [1,-1], [-1,-2]])
    test.run()
    test.time()

    # Test `unit_propagate` function
    test_2 = Test(unit_propagate, [[[1], [-1,2]]], [])
    test_2.run()
    test_2.time()

    # Test `simple_sat_solve` function
    test_3 = Test(simple_sat_solve, [[[1],[1,-1],[-1,-2]]], [1,-2])
    test_3.run()
    test_3.time()
