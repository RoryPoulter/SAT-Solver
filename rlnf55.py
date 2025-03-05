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
    return [x if x > 0 else -x for x in set(chain(*clause_set))]


def choose_literal(clause_set: list[list[int]]) -> int:
    """Chooses the most common literal in the clause-set

    Args:
        clause_set (list[list[int]]): The clause-set

    Returns:
        int: The most common literal
    """
    flat_list = list(chain(*clause_set))
    return max(flat_list, key=flat_list.count)


def remove_clauses(clause_set: list[list[int]], literal: int) -> list[list[int]]:
    """Removes satisfied clauses and instances of negative literal in clauses

    Args:
        clause_set (list[list[int]]): The original clause-set
        literal (int): The literal

    Returns:
        list[list[int]]: The reduced clause-set
    """
    new_clause_set = []
    for clause in clause_set:
        if -literal in clause and literal not in clause:
            clause.remove(-literal)
            new_clause_set.append(clause)
        elif literal not in clause:
            new_clause_set.append(clause)
    return new_clause_set


def pure_literal_elimination(clause_set: list[list[int]], literals: int) -> list[list[int]]:
    """Performs pure literal elimination on a clause-set

    Args:
        clause_set (list[list[int]]): The original clause-set
        literals (int): The number of literals in the clause-set

    Returns:
        list[list[int]]: The reduced clause-set
    """
    for i in range(1, literals + 1):
        # Lists for clauses which contain only positive and negative literal respectively
        pos_clauses = []
        neg_clauses = []
        pure_literals = []
        # Iterate for every clause in the clause-set
        for clause in clause_set:
            if i in clause and -i not in clause:
                pos_clauses.append(clause)
                pure_literals.append(i)
            elif -i in clause and i not in clause:
                neg_clauses.append(clause)
                pure_literals.append(-i)
            # If not a pure literal, break loop and move to next i
            if pos_clauses and neg_clauses:
                break
        # If i / ¬i is a pure literal
        else:
            if pos_clauses:
                for clause in pos_clauses:
                    clause_set.remove(clause)
            elif neg_clauses:
                for clause in neg_clauses:
                    clause_set.remove(clause)
    return clause_set, pure_literals


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
        list[int] | bool: The assignment of literals if satisfiable, `False` if unsatisfiable
    """
    # If partial_assignment is not empty, i.e. != []
    if partial_assignment:
        clause_set = remove_clauses(clause_set, partial_assignment[-1])

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
        list[int] | bool: _description_
    """
    print(clause_set, partial_assignment)
    literals = number_of_literals(clause_set)
    clause_set = unit_propagate(clause_set)
    clause_set, pure_literals = pure_literal_elimination(clause_set, literals)
    partial_assignment += pure_literals

    literal = choose_literal(clause_set)
    print(literal)


if __name__ == "__main__":
    PATH = "Examples/Examples-for-SAT/PHP-5-4.txt"
    example_clause_set = load_dimacs(PATH)
    if example_clause_set is None:
        sys.exit()
    print("\n***********Simple SAT Solve***********\n")
    print(example_clause_set)
    print(simple_sat_solve(example_clause_set))
    print("\n***********Branching SAT Solve***********\n")
    print(example_clause_set)
    print(branching_sat_solve(example_clause_set, partial_assignment=[]))
