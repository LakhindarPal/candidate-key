# Theory Behind the Optimized Candidate Key Discovery Method

## Key Concepts

Given:
- A relation `R`
- A set of functional dependencies `F`

We define:

- **Must-Have Attributes (M)**:  
  `M = R - RHS(F)`  
  These attributes **cannot be derived** from any FD, so **must be included** in every candidate key.

- **Helper Attributes (H)**:  
  `H = LHS(F) - M`  
  These are the only useful attributes for expanding M to a superkey.

---

## Optimized Algorithm

1. Compute `M = R - RHS(F)`
2. If `closure(M) == R`, then `M` is a candidate key.
   - If so, it's the **only candidate key** (see proof below).
3. Else, generate all subsets of `H = LHS(F) - M`
4. Combine each subset `S ⊆ H` with `M`, check closure.
5. If `closure(M ∪ S) == R`, it's a superkey. Keep only **minimal** superkeys as candidate keys.
6. Skip all supersets once a candidate key is found (early stopping).

---

## Why Only One Candidate Key if `M` is a Key?

- By definition, attributes in `M` cannot be derived.
- If `M+ == R`, then no attribute can be removed from `M` without losing closure.
- Therefore, `M` is already minimal and sufficient — **a unique candidate key**.

---

## Why Only Subsets of `LHS - M` Are Checked?

- Attributes in `RHS-only` are derivable and don’t help in reaching other attributes.
- `LHS - M` contains those that can help derive remaining attributes.
- Combining `M` with subsets of this set covers all useful derivation chains without unnecessary checks.

---

## Efficiency

This approach reduces the search space from `2^|R|` (in brute force) to at most `2^|LHS - M|`, which is often dramatically smaller.

---

## Example

### Input
R = {A, B, C, D, E}  
FDs = {A→D, B→A, BC→D, AC→BE}

### Step 1: Compute
- RHS = {D, A, D, B, E} = {A, B, D, E}
- M = R - RHS = {C}
- LHS = {A, B, BC, AC} → LHS attrs = {A, B, C}
- H = LHS - M = {A, B}

### Step 2: Try:
- M = {C}
  - `closure(C)` = {C} — not enough
- Try M ∪ subsets of H:
  - {A, C} → closure = {A, C, B, D, E} = R → candidate key!
  - {B, C} → also works

→ Candidate Keys: AC, BC

---

## Empirical Evidence

Results show that the optimized method:
- Matches brute-force output in all tested cases
- Runs significantly faster
- Uses less memory

---

## Conclusion

This technique demonstrates a more intelligent approach to candidate key discovery, grounded in the structure of FDs.