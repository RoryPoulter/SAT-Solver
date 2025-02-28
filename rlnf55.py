"""SAT solver for Computational Thinking Logic Coursework
"""


def load_dimacs(path: str) -> list[list[int]]:
    """Loads a file in DIMACS format and returns the clause-set

    Args:
        path (str): The path to the file

    Returns:
        list[list[int]]: The clause-set
    """
    with open(path, "r", encoding="utf-8") as file:
        data = file.readlines()
    lines = [x.split(" ")[:-1] for x in data][1:]
    clause_set = [[int(x) for x in num] for num in lines]
    return clause_set


def simple_sat_solve(clause_set: list[list[int]]) -> list[int] | bool:
    """SAT solver that uses brute force to check every literal assignment until either a satisfying
    assignment is found or all have been checked

    Args:
        clause_set (list[list[int]]): The clause-set to be checked

    Returns:
        list[int] | False: The assignment of literals if satisfiable, `False` if unsatisfiable
    """
    print(clause_set)


def branching_sat_solve(clause_set: list[list[int]],
                        partial_assignment: list[int]) -> list[int] | bool:
    """Recursive function for SAT solving

    Args:
        clause_set (list[list[int]]): The clause-set to be checked
        partial_assignment (list[int]): _description_

    Returns:
        list[int] | False: The assignment of literals if satisfiable, `False` if unsatisfiable
    """
    print(clause_set, partial_assignment)


def unit_propagate(clause_set: list[list[int]]) -> list[list[int]]:
    """Performs unit propagation on a clause-set to find simplified clause-set 

    Args:
        clause_set (list[list[int]]): The original clause-set

    Returns:
        list[list[int]]: The simplified clause-set
    """
    print(clause_set)


def dpll_sat_solve(clause_set: list[list[int]], partial_assignment: list[int]) -> list[int] | bool:
    """_summary_

    Args:
        clause_set (list[list[int]]): _description_
        partial_assignment (list[int]): _description_

    Returns:
        list[int] | False: _description_
    """
    print(clause_set, partial_assignment)


if __name__ == "__main__":
    PATH = "Examples/sat.txt"
    example_clause_set = load_dimacs(PATH)
