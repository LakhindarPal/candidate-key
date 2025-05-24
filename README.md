# Candidate Key Discovery: Optimized vs Brute Force

This project explores an efficient algorithm to compute **candidate keys** in a relational schema. It compares a classic brute-force method with a novel optimization strategy that significantly reduces the search space.

## Features

- Generates random relations and functional dependencies
- Compares two algorithms:
  - **Brute-force**: Checks closure of all attribute subsets
  - **Optimized**: Starts from essential attributes and smartly limits the search space
- Measures execution time
- Outputs CSV report for easy analysis

## Installation

```bash
git clone https://github.com/LakhindarPal/candidate-key.git
cd candidate-key
```
## Usage

Run the experiment with defaults:

`python main.py`

Customize runs:

`run_parallel_csv(cases=500, attr_min=4, attr_max=7)`

Output Format

CSV columns:

Relation (comma-separated)

FDs (e.g., A→BC)

Brute-force Candidate Keys

Optimized Candidate Keys

Remark (Match / Mismatch)

Time (ms) for both methods


## Theory

See [THEORY.md](THEORY.md) for full explanation of the optimized algorithm, reasoning, and proofs.

## License
[MIT](LICENSE)