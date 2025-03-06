"""Test file for rlnf55.py
"""


from timeit import default_timer as timer
from rlnf55 import (load_dimacs, unit_propagate, simple_sat_solve, branching_sat_solve,
                    dpll_sat_solve)


class Test:
    """Class for running tests
    """
    def __init__(self, func, args: list, output):
        self.func = func
        self.args = args
        self.output = output
        self.is_correct = self.run()
        if self.is_correct:
            self.time(1)

    def run(self) -> bool:
        """Runs the function with the given arguments and compares the result with the expected
        output.

        Returns:
            bool: If the function produced the correct output
        """
        print(f"Testing function {self.func.__name__}")
        try:
            result = self.func(*self.args)
            assert result == self.output
            print("    ✓ Function works")
            return True
        except AssertionError:
            print(f"    X Function does not work: returned {result}, expected {self.output}")
            return False

    def time(self, iters: int = 1000) -> None:
        """Measures the time elapsed for a function to execute a given number of times

        Args:
            iters (int, optional): The number of execution iterations. Defaults to 1000.
        """
        start = timer()
        for _ in range(iters):
            __ = self.func(*self.args)
        end = timer()
        time_elapsed = end - start
        print(f"    Function took {time_elapsed}s to execute {iters} times")


if __name__ == "__main__":
    print("========== Start Testing ==========")
    # Test `load_dimacs` function
    test_1 = Test(load_dimacs, ["Examples/sat.txt"], [[1], [1,-1], [-1,-2]])

    # Test `unit_propagate` function
    test_2 = Test(unit_propagate, [[[1], [-1,2]]], [])

    # Test `simple_sat_solve` function
    test_3_a = Test(simple_sat_solve, [[[1], [1,-1], [-1,-2]]], [1,-2])
    test_3_b = Test(simple_sat_solve, [[[1,2], [-1,2], [-1,-2], [1,-2]]], False)

    # Test `branching_sat_solve` function
    test_4_a = Test(branching_sat_solve, [[[1], [1,-1], [-1,-2]], []], [1, -2])
    test_4_b = Test(branching_sat_solve, [[[1,2], [-1,2], [-1,-2], [1,-2]], []], False)

    # Test `dpll_sat_solve` function
    test_5_a = Test(dpll_sat_solve, [[[1], [1,-1], [-1,-2]], []], [1, -2])
    test_5_b = Test(dpll_sat_solve, [[[1,2], [-1,2], [-1,-2], [1,-2]], []], False)

    all_tests = {test_1, test_2, test_3_a, test_3_b, test_4_a, test_4_b, test_5_a, test_5_b}
    passed_tests = {test for test in all_tests if test.is_correct}
    print(f"""===================================
Pass rate: {100 * len(passed_tests) / len(all_tests)}""")
