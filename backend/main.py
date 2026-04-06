"""
main.py

Entry point for Sudoku AI Solver Pro.

Features:
- Backtracking + CSP
- MRV + Degree Heuristic
- Clean architecture for extensibility
- CLI-friendly execution

Author: YourName
"""

from typing import List, Set, Tuple
from copy import deepcopy
import time

# Import heuristics
from heuristics.degree import select_variable_with_degree

Board = List[List[int]]


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def print_board(board: Board) -> None:
    """
    Pretty-print the Sudoku board.
    """
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            print(board[i][j] if board[i][j] != 0 else ".", end=" ")

        print()
    print()


def is_valid(board: Board, row: int, col: int, num: int) -> bool:
    """
    Check if placing 'num' at (row, col) is valid.
    """

    # Row
    if any(board[row][i] == num for i in range(9)):
        return False

    # Column
    if any(board[i][col] == num for i in range(9)):
        return False

    # Subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True


def initialize_domains(board: Board) -> List[List[Set[int]]]:
    """
    Initialize domains for each cell.
    """
    domains = [[set() for _ in range(9)] for _ in range(9)]

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                domains[row][col] = {
                    num for num in range(1, 10)
                    if is_valid(board, row, col, num)
                }
            else:
                domains[row][col] = {board[row][col]}

    return domains


# ---------------------------------------------------------------------------
# CSP Solver (Backtracking + MRV + Degree)
# ---------------------------------------------------------------------------

def solve_sudoku(board: Board) -> Tuple[bool, int]:
    """
    Solve Sudoku using CSP + heuristics.

    Returns:
        (solved: bool, steps: int)
    """

    domains = initialize_domains(board)
    steps = 0

    def backtrack() -> bool:
        nonlocal steps

        # Check if solved
        if all(board[row][col] != 0 for row in range(9) for col in range(9)):
            return True

        # Select variable using MRV + Degree
        row, col = select_variable_with_degree(board, domains)

        for value in sorted(domains[row][col]):
            if is_valid(board, row, col, value):
                board[row][col] = value
                steps += 1

                # Save domains state (for backtracking)
                saved_domains = deepcopy(domains)

                # Forward Checking: update domains
                for r in range(9):
                    if value in domains[r][col]:
                        domains[r][col].discard(value)
                for c in range(9):
                    if value in domains[row][c]:
                        domains[row][c].discard(value)

                start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        if value in domains[r][c]:
                            domains[r][c].discard(value)

                # Recursive step
                if backtrack():
                    return True

                # Undo (backtrack)
                board[row][col] = 0
                domains[:] = saved_domains

        return False

    solved = backtrack()
    return solved, steps


# ---------------------------------------------------------------------------
# Example Run
# ---------------------------------------------------------------------------

def main():
    """
    Main execution entry.
    """

    # Example Sudoku (0 = empty)
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("🧩 Initial Sudoku:\n")
    print_board(board)

    start_time = time.time()

    solved, steps = solve_sudoku(board)

    end_time = time.time()

    if solved:
        print("✅ Solved Sudoku:\n")
        print_board(board)
    else:
        print("❌ No solution found.")

    print(f"⏱ Time: {(end_time - start_time):.4f}s")
    print(f"🔢 Steps: {steps}")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
