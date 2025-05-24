import itertools
import random
import time
import csv
from typing import List, Set, Tuple
from concurrent.futures import ProcessPoolExecutor


def powerset(s: List[str]) -> List[Set[str]]:
    """Generates all subsets of a list"""
    return [set(c) for i in range(len(s) + 1) for c in itertools.combinations(s, i)]


def closure(attrs: Set[str], fds: List[Tuple[Set[str], Set[str]]]) -> Set[str]:
    result = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs.issubset(result) and not rhs.issubset(result):
                result.update(rhs)
                changed = True
    return result


def ck_brute(
    relation: Set[str], fds: List[Tuple[Set[str], Set[str]]]
) -> List[Set[str]]:
    keys = []
    seen = set()
    for subset in sorted(powerset(list(relation)), key=len):
        fs = frozenset(subset)
        if any(fs.issuperset(k) for k in seen):
            continue
        if closure(subset, fds) == relation:
            keys.append(subset)
            seen.add(fs)
    return keys


def ck_optimized(
    relation: Set[str], fds: List[Tuple[Set[str], Set[str]]]
) -> List[Set[str]]:
    rhs = {a for _, r in fds for a in r}
    lhs = {a for l, _ in fds for a in l}
    M = relation - rhs
    H = lhs - M
    keys = []
    seen = set()
    for sub in sorted(powerset(list(H)), key=len):
        key_candidate = M.union(sub)
        fs = frozenset(key_candidate)
        if any(fs.issuperset(k) for k in seen):
            continue
        if closure(key_candidate, fds) == relation:
            keys.append(key_candidate)
            seen.add(fs)
    return keys


def generate_fd(attributes: List[str], max_fds=6) -> List[Tuple[Set[str], Set[str]]]:
    return [
        (
            set(random.sample(attributes, random.randint(1, 2))),
            set(random.sample(attributes, random.randint(1, 2))),
        )
        for _ in range(random.randint(3, max_fds))
    ]


def format_fds(fds: List[Tuple[Set[str], Set[str]]]) -> str:
    return ", ".join(
        f"{''.join(sorted(lhs))}->{''.join(sorted(rhs))}" for lhs, rhs in fds
    )


def format_cks(cks: List[Set[str]]) -> str:
    return ", ".join("".join(sorted(ck)) for ck in cks)


def run_case(case_no: int, attr_min: int, attr_max: int):
    attr_count = random.randint(attr_min, attr_max)
    attributes = [chr(65 + i) for i in range(attr_count)]
    relation = set(attributes)
    fds = generate_fd(attributes)

    t0 = time.perf_counter()
    brute = ck_brute(relation, fds)
    t1 = time.perf_counter()
    opt = ck_optimized(relation, fds)
    t2 = time.perf_counter()

    brute_time = (t1 - t0) * 1000
    opt_time = (t2 - t1) * 1000

    b_set = {frozenset(x) for x in brute}
    o_set = {frozenset(x) for x in opt}
    remark = "Match" if b_set == o_set else "Mismatch"

    return [
        case_no,
        ",".join(sorted(relation)),
        format_fds(fds),
        format_cks(brute),
        format_cks(opt),
        remark,
        f"{brute_time:.2f}",
        f"{opt_time:.2f}",
    ]


def run_parallel_csv(output_file="report.csv", cases=1000, attr_min=4, attr_max=7):
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(run_case, i + 1, attr_min, attr_max) for i in range(cases)
        ]
        results = [f.result() for f in futures]

    with open(output_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Case",
                "Relation",
                "FDs",
                "Brute-force CKs",
                "Optimized CKs",
                "Remark",
                "Brute_time_ms",
                "Opt_time_ms",
            ]
        )
        writer.writerows(results)

    matches = sum(1 for row in results if row[5] == "Match")
    print(f"Done: {matches}/{cases} match ({matches/cases*100:.2f}%)")


if __name__ == "__main__":
    run_parallel_csv(cases=1000000)
