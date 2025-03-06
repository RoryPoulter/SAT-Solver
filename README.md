# SAT-Solver

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/RoryPoulter/SAT-Solver/pylint.yml?style=for-the-badge&logo=python&logoColor=%23ffffff)
![GitHub last commit](https://img.shields.io/github/last-commit/RoryPoulter/SAT-Solver?style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/RoryPoulter/SAT-Solver?style=for-the-badge)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/RoryPoulter/SAT-Solver?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/RoryPoulter/SAT-Solver?style=for-the-badge)



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
* `simple_sat_solve(clause_set)` - SAT solver that uses brute force to check every assignment until either a satisfying assignment is found or all have been checked
* `branching_sat_solve(clause_set, partial_assignment)` - SAT solver that uses recursion to branch on each literal
* `dpll_sat_solve(clause_set, partial_assignment)` - SAT solver that uses the DPLL algorithm
```py
import rlnf55 as ss


if __name__ == "__main__":
    PATH = "relative/path/to/file"
    # Load the DIMACs file
    clause_set = ss.load_dimacs(PATH)
    # Use SAT solver to find satisfying assignment of if clause-set is unsatisfiable
    assignment = ss.dpll_sat_solve(clause_set, [])
    if assignment:
        print(f"Clause-set from {PATH} is satisfiable under the assignment: {assignment}.")
    else:
        print(f"Clause-set from {PATH} is unsatisfiable.")
```