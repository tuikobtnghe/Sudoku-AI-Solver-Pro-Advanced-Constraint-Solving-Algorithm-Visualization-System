"""
mrv.py

Implementation of Minimum Remaining Values (MRV) heuristic for Sudoku CSP.

MRV selects the variable (cell) with the smallest number of possible values,
reducing branching factor and improving search efficiency.

Author: tuikobtnghe & master: kennz_psix
"""

from typing import List, Set, Tuple, Optional

Board = List[List[int]]
Domains = List[List[Set[int]]]


# ---------------------------------------------------------------------------
# MRV Core
# ---------------------------------------------------------------------------

def find_mrv_cell(
    board: Board,
    domains: Domains
) -> Optional[Tuple[int, int]]:
    """
    Find the unassigned variable with the minimum remaining values (MRV).

    Args:
        board: Sudoku board
        domains: domain grid

    Returns:
        (row, col) of selected cell, or None if all assigned
    """

    min_domain_size = float("inf")
    best_cell = None

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                domain_size = len(domains[row][col])

                # Fail-fast: empty domain → dead end
                if domain_size == 0:
                    return (row, col)

                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    best_cell = (row, col)

    return best_cell


# ---------------------------------------------------------------------------
# MRV with Tie-Breaking Hook (Degree integration-ready)
# ---------------------------------------------------------------------------

def find_mrv_with_tiebreak(
    board: Board,
    domains: Domains,
    degree_fn=None
) -> Tuple[int, int]:
    """
    MRV with optional tie-breaking using Degree Heuristic.

    Args:
        board: Sudoku board
        domains: domain grid
        degree_fn: function(board, row, col) -> int

    Returns:
        (row, col)
    """

    candidates = []

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                domain_size = len(domains[row][col])

                if domain_size == 0:
                    return (row, col)

                if degree_fn:
                    degree = degree_fn(board, row, col)
                else:
                    degree = 0

                # Sort by:
                # 1. smallest domain (MRV)
                # 2. highest degree (tie-break)
                candidates.append((domain_size, -degree, row, col))

    if not candidates:
        raise ValueError("No unassigned variables found.")

    candidates.sort()
    _, _, r, c = candidates[0]

    return r, c


# ---------------------------------------------------------------------------
# Optional: Domain Statistics (for analysis)
# ---------------------------------------------------------------------------

def get_domain_stats(domains: Domains) -> dict:
    """
    Return statistics about domain distribution.

    Useful for debugging or performance analysis.
    """
    sizes = [len(domains[r][c]) for r in range(9) for c in range(9)]

    return {
        "min": min(sizes),
        "max": max(sizes),
        "avg": sum(sizes) / len(sizes),
        "empty": sum(1 for s in sizes if s == 0)
    }


# ---------------------------------------------------------------------------
# Debug / Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example board
    board = [[0]*9 for _ in range(9)]

    # Example domains
    domains = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]

    # Simulate constraints
    domains[0][0] = {1, 2}
    domains[0][1] = {3}
    domains[1][0] = {4, 5, 6}

    cell = find_mrv_cell(board, domains)
    print(f"MRV selected cell: {cell}")

    stats = get_domain_stats(domains)
    print("Domain stats:", stats)
