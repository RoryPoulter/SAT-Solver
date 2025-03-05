# SAT-Solver

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/RoryPoulter/SAT-Solver/pylint.yml)
![GitHub last commit](https://img.shields.io/github/last-commit/RoryPoulter/SAT-Solver)
![GitHub License](https://img.shields.io/github/license/RoryPoulter/SAT-Solver)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/RoryPoulter/SAT-Solver)


SAT Solver for Computational Thinking Coursework.

## Usage
### Using the `rlnf55.py` File
* Write a .txt file in DIMACs format for the clause-set
* Set the `PATH` constant to the path to the file relative to `rlnf55.py`, e.g.

```python
PATH = "Examples\Examples-for-SAT\LNP-6.txt"
```
* Run `rlnf55.py`

### Importing `rlnf55.py`
Functions to import:
* `load_dimacs(PATH)` - Loads a .txt file in DIMACs format and generates the corresponding clause-set
* `simple_sat_solve(clause_set)` - SAT solver that uses brute force to check eveyr assignment until either a satisfying assignment is found or all have been checked
* `branching_sat_solve(clause_set, partial_assignment)` - SAT solver that uses recursion to branch on each literal
* `dpll_sat_solve(clause_set, partial_assignment)` - SAT solver that uses the DPLL algorithm
```py
import rlnf55 as ss


if __name__ == "__main__":
    PATH = <path-to-DIMACS-file-here>
    clause_set = ss.load_dimacs(PATH)
    assignment = ss.dpll_sat_solve(clause_set, [])
    if assignment:
        print(f"Clause-set from {PATH} is satisfiable under the assignment: {assignment}.")
    else:
        print(f"Clause-set from {PATH} is unsatisfiable.")
```