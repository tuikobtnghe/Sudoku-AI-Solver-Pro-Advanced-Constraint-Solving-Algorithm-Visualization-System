"""
lcv.py

Implementation of Least Constraining Value (LCV) heuristic for Sudoku CSP.

LCV selects values that eliminate the fewest options for neighboring variables,
thereby preserving flexibility and reducing future conflicts.

Author: YourName
"""

from typing import List, Set, Tuple

Board = List[List[int]]
Domains = List[List[Set[int]]]


# ---------------------------------------------------------------------------
# Utility: Get peers
# ---------------------------------------------------------------------------

def get_peers(row: int, col: int) -> Set[Tuple[int, int]]:
    """
    Return all peer cells of (row, col).
    """
    peers = set()

    # Row & Column
    for i in range(9):
        if i != col:
            peers.add((row, i))
        if i != row:
            peers.add((i, col))

    # Subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r, c) != (row, col):
                peers.add((r, c))

    return peers


# ---------------------------------------------------------------------------
# LCV Core
# ---------------------------------------------------------------------------

def count_constraints(
    domains: Domains,
    row: int,
    col: int,
    value: int
) -> int:
    """
    Count how many domain values would be eliminated from neighbors
    if 'value' is assigned to (row, col).

    Lower count = better (less constraining).
    """
    impact = 0

    for r, c in get_peers(row, col):
        if value in domains[r][c]:
            impact += 1

    return impact


def order_values_lcv(
    board: Board,
    domains: Domains,
    row: int,
    col: int
) -> List[int]:
    """
    Return values for (row, col) ordered by Least Constraining Value.

    Strategy:
    - Values that constrain neighbors the least come first

    Args:
        board: Sudoku board
        domains: domain grid
        row, col: target cell

    Returns:
        List of values sorted by LCV
    """

    if board[row][col] != 0:
        return [board[row][col]]

    values = list(domains[row][col])

    # Sort by constraint impact (ascending)
    values.sort(key=lambda v: count_constraints(domains, row, col, v))

    return values


# ---------------------------------------------------------------------------
# Optional: Detailed scoring (for analysis/debug)
# ---------------------------------------------------------------------------

def score_values_lcv(
    domains: Domains,
    row: int,
    col: int
) -> List[Tuple[int, int]]:
    """
    Return (value, impact score) for debugging or visualization.

    Lower score = better choice.
    """
    scores = []

    for value in domains[row][col]:
        impact = count_constraints(domains, row, col, value)
        scores.append((value, impact))

    # Sort by least impact
    scores.sort(key=lambda x: x[1])

    return scores


# ---------------------------------------------------------------------------
# Debug / Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example domains
    domains = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]

    # Simulate constraints
    domains[0][1] = {1}
    domains[1][0] = {2}
    domains[1][1] = {3}

    row, col = 0, 0

    print("LCV order:")
    print(order_values_lcv([[0]*9 for _ in range(9)], domains, row, col))

    print("\nDetailed scores:")
    print(score_values_lcv(domains, row, col))
