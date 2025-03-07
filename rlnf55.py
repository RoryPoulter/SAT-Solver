"""SAT solver for Computational Thinking Logic Coursework
"""


# Import required libraries
from itertools import product, chain
import sys
from copy import deepcopy


def get_all_literals(clause_set: list[list[int]]) -> list[int]:
    """Creates list of literals from clause-set

    Args:
        clause_set (list[list[int]]): The clause-set

    Returns:
        list[int]: The list of remaining literals
    """
    return list({x if x > 0 else -x for x in set(chain(*clause_set))})


def choose_literal(clause_set: list[list[int]]) -> int:
    """Chooses the most common literal in the clause-set

    Args:
        clause_set (list[list[int]]): The clause-set

    Returns:
        int: The most common literal
    """
    flat_list = list(chain(*clause_set))
    return max(flat_list, key=flat_list.count)


def remove_clauses(clause_set: list[list[int]], assignment: list[int]) -> list[list[int]]:
    """Removes satisfied clauses and instances of negative literal in clauses

    Args:
        clause_set (list[list[int]]): The original clause-set
        assignment (list[int]): The assignment

    Returns:
        list[list[int]]: The reduced clause-set
    """
    new_clause_set = []
    assignment_set = set(assignment)
    neg_assignment_set = {-x for x in assignment_set}
    for clause in clause_set:
        clause_s = set(clause)
        if assignment_set & clause_s:
            pass
        elif neg_assignment_set & clause_s:
            clause = list(clause_s - neg_assignment_set)
            new_clause_set.append(clause)
        elif not assignment_set & clause_s:
            new_clause_set.append(clause)
    return new_clause_set


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
        list[int] | bool: The assignment of literals if satisfiable, `False` if unsatisfiable
    """
    literals = get_all_literals(clause_set)
    pos_neg_pairs = [[x, -x] for x in literals]
    all_assignments = product(*pos_neg_pairs)
    for assignment in all_assignments:
        if check_satisfies(clause_set, assignment):
            return list(assignment)
    return False


def branching_sat_solve(clause_set: list[list[int]],
                        partial_assignment: list[int] = None) -> list[int] | bool:
    """Recursive function for SAT solving

    Args:
        clause_set (list[list[int]]): The clause-set to be checked
        partial_assignment (list[int]): The assignment at the stage the function is called

    Returns:
        list[int] | bool: The assignment of literals if satisfiable, `False` if unsatisfiable
    """
    # If partial_assignment is not empty, i.e. != []
    if partial_assignment:
        clause_set = remove_clauses(clause_set, partial_assignment)
    else:
        partial_assignment = []

    # Check clause-set is satisfied
    if not clause_set:
        return partial_assignment

    # Check clause-set has empty clause
    if [] in clause_set:
        return False

    # Choose the next literal to branch off of
    literal = get_all_literals(clause_set)[0]

    partial_assignment.append(literal)
    partial_assignment_2 = deepcopy(partial_assignment)
    partial_assignment_2[-1] *= -1
    clause_set_2 = deepcopy(clause_set)
    pos_result = branching_sat_solve(clause_set, partial_assignment)
    neg_result = branching_sat_solve(clause_set_2, partial_assignment_2)
    return pos_result or neg_result


def unit_propagate(clause_set: list[list[int]]) -> list[list[int]]:
    """Performs unit propagation on a clause-set to find simplified clause-set 

    Args:
        clause_set (list[list[int]]): The original clause-set

    Returns:
        list[list[int]]: The simplified clause-set
    """
    all_unit_clauses = []
    unit_clauses = [clause[0] for clause in clause_set if len(clause) == 1]
    all_unit_clauses += unit_clauses
    while unit_clauses:
        literal = unit_clauses.pop()
        new_clause_set = []
        for clause in clause_set:
            if literal in clause:
                continue
            if -literal in clause:
                clause.remove(-literal)
                if len(clause) == 1:
                    unit_clauses.append(clause[0])
                else:
                    new_clause_set.append(clause)
            else:
                new_clause_set.append(clause)
        clause_set = new_clause_set
    return clause_set


def up(clause_set: list[list[int]]) -> tuple[list]:
    """Unit propagation for DPLL SAT solver

    Args:
        clause_set (list[list[int]]): The clause-set

    Returns:
        tuple[list]: Tuple with the reduced clause set and set of literals to reduce clause-set
    """
    all_unit_clauses = []
    unit_clauses = list({clause[0] for clause in clause_set if len(clause) == 1})
    all_unit_clauses += unit_clauses
    while unit_clauses:
        new_clause_set = []
        unit_clause = unit_clauses.pop()

        if -unit_clause in all_unit_clauses:
            return [[]], []

        for clause in clause_set:
            if unit_clause in clause:
                continue
            if -unit_clause in clause:
                clause.remove(-unit_clause)
                if len(clause) == 1:
                    unit_clauses.append(clause[0])
                    all_unit_clauses.append(clause[0])
                else:
                    new_clause_set.append(clause)
            else:
                new_clause_set.append(clause)
        clause_set = new_clause_set

    return clause_set, all_unit_clauses


def dpll_sat_solve(clause_set: list[list[int]],
                   partial_assignment: list[int] = None) -> list[int] | bool:
    """SAT solver using DPLL algorithm without pure literal elimination

    Args:
        clause_set (list[list[int]]): The clause-set
        partial_assignment (list[int]): The assignment at the stage the function is called

    Returns:
        list[int] | bool: Either a satisfying assignment of literals, or `False` if unsatisfiable
    """
    if partial_assignment is None:
        partial_assignment = []
    # Perform unit propagation on clause-set
    clause_set, unit_literals = up(clause_set)
    partial_assignment += unit_literals
    # If partial_assignment is not empty, i.e. != []
    if partial_assignment:
        clause_set = remove_clauses(clause_set, partial_assignment)

    # Check clause-set is satisfied
    if not clause_set:
        return partial_assignment

    # Check clause-set has empty clause
    if [] in clause_set:
        return False

    literal = choose_literal(clause_set)
    partial_assignment.append(literal)
    partial_assignment_2 = deepcopy(partial_assignment)
    partial_assignment_2[-1] *= -1
    clause_set_2 = deepcopy(clause_set)
    pos_result = dpll_sat_solve(clause_set, partial_assignment)
    neg_result = dpll_sat_solve(clause_set_2, partial_assignment_2)
    return pos_result or neg_result


if __name__ == "__main__":
    PATH = "Examples/unsat.txt"
    example_clause_set = load_dimacs(PATH)
    if example_clause_set is None:
        sys.exit()
    print("\n***********DPLL SAT Solve***********\n")
    print(example_clause_set)
    print(dpll_sat_solve(example_clause_set, partial_assignment=[]))
