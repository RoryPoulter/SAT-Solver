"""SAT solver for Computational Thinking Logic Coursework
"""


# Import required libraries
from itertools import product
import sys


def check_satisfies(clause_set: list[list[int]], assignment: list[int]) -> bool:
    """Checks if an assignment satisfies a clause-set

    Args:
        clause_set (list[list[int]]): The clause-set to be satisfied
        assignment (list[int]): The assignment to be tested

    Returns:
        bool: If the assignment is satisfying
    """
    for literal in assignment:
        # Creates new clause-set with satisfied clauses removed
        new_clause_set = []
        for clause in clause_set:
            # Only append unsatisfied clauses
            if literal not in clause:
                new_clause_set.append(clause)
        clause_set = new_clause_set
        if not clause_set:
            return True
    return False


def number_of_literals(clause_set: list[list[int]]) -> int:
    """Finds the number of literals in a clause-set

    Args:
        clause_set (list[list[int]]): The clause-set to be checked

    Returns:
        int: The number of literals
    """
    all_literals = set()
    for clause in clause_set:
        literals = {x if x > 0 else x*-1 for x in clause}
        all_literals |= literals
    return len(all_literals)


def load_dimacs(path: str) -> list[list[int]] | None:
    """Loads a file in DIMACS format and returns the clause-set

    Args:
        path (str): The path to the file

    Returns:
        list[list[int]] | None: The clause-set, `None` if the file is not found
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = file.readlines()
    except FileNotFoundError:
        print(f"File '{path}' not found")
        return None
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
    literals = number_of_literals(clause_set)
    pos_neg_pairs = [[x, -x] for x in range(1, literals+1)]
    all_assignments = product(*pos_neg_pairs)
    for assignment in all_assignments:
        if check_satisfies(clause_set, assignment):
            return list(assignment)
    return False


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
    # Find all unit clauses
    all_unit_clauses = []
    for clause in clause_set:
        if len(clause) == 1:
            all_unit_clauses.append(clause)
    # Iterate for each unit clause
    for unit_clause in all_unit_clauses:
        clause_set.remove(unit_clause)
        val = unit_clause[0]
        neg_val = val * -1
        for clause in clause_set:
            # Remove clauses containing the unit literal
            if val in clause or neg_val in clause:
                clause_set.remove(clause)
    return clause_set


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
    PATH = "Examples/Examples-for-SAT/W_2,3_ n=8.txt"
    example_clause_set = load_dimacs(PATH)
    if example_clause_set is None:
        sys.exit()
    reduced_clause_set = unit_propagate(example_clause_set)
    print(simple_sat_solve(reduced_clause_set))
