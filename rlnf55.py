"""SAT solver for Computational Thinking Logic Coursework
"""


def load_dimacs(path: str) -> list[list[int]]:
    """Loads a file in DIMACS format and returns the clause-set

    Args:
        path (str): The path to the file

    Returns:
        list[list[int]]: The clause-set
    """


def simple_sat_solve(clause_set: list[list[int]]) -> list[int] | False:
    """SAT solver that uses brute force to check every literal assignment until either a satisfying
    assignment is found or all have been checked

    Args:
        clause_set (list[list[int]]): The clause-set to be checked

    Returns:
        list[int] | False: The assignment of literals if satisfiable, `False` if unsatisfiable
    """


def branching_sat_solve(clause_set: list[list[int]], partial_assignment: list[int]) -> list[int] | False:
    """Recursive function for SAT solving

    Args:
        clause_set (list[list[int]]): The clause-set to be checked
        partial_assignment (list[int]): _description_

    Returns:
        list[int] | False: The assignment of literals if satisfiable, `False` if unsatisfiable
    """


def unit_propagate(clause_set: list[list[int]]) -> list[list[int]]:
    """Performs unit propagation on a clause-set to find simplified clause-set 

    Args:
        clause_set (list[list[int]]): The original clause-set

    Returns:
        list[list[int]]: The simplified clause-set
    """


def dpll_sat_solve(clause_set: list[list[int]], partial_assignment: list[int]) -> list[int] | False:
    """_summary_

    Args:
        clause_set (list[list[int]]): _description_
        partial_assignment (list[int]): _description_

    Returns:
        list[int] | False: _description_
    """


if __name__ == "__main__":
    pass
