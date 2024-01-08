#sudoku_solver.py
"""
Module for solving Sudoku puzzles.

This module includes the SudokuSolver class, which is responsible for solving
Sudoku puzzles and checking the validity of solutions.
"""

class SudokuSolver:
    """
    Class for solving Sudoku puzzles.

    Attributes:
        board (list): A 10x10 grid representing the Sudoku board.
    """
    
    def __init__(self, board):
        """
        Initialize the SudokuSolver with a given Sudoku board.

        Args:
            board (list): A 10x10 grid representing the Sudoku board.
        """
        self.board = board

    def solve(self):
        """
        Solve the Sudoku puzzle using a backtracking algorithm.

        Returns:
            bool: True if a solution is found, False otherwise.

        This method attempts to solve the Sudoku puzzle using a backtracking
        algorithm. It modifies the internal state of the SudokuSolver object.
        """
        empty_cell = (0, 0)
        if not self._find_empty_cell(empty_cell):
            return True

        row, col = empty_cell
        for num in range(1, 11):
            if self._is_valid_move(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0

        return False

    def is_unique_solution(self, original_board):
        """
        Check if the Sudoku puzzle has a unique solution.

        Args:
            original_board (list): The original state of the Sudoku board.

        Returns:
            bool: True if the solution is unique, False otherwise.

        This method checks whether the current Sudoku board has a unique
        solution by attempting to solve it and counting the number of
        solutions.
        """
        solution_count = 0
        self.board = [row[:] for row in original_board]
        self.solve()
        return solution_count == 1

    def _is_valid_row(self, row, num):
        """
        Check if placing a number in a specific row is a valid move.

        Args:
            row (int): The row index of the cell.
            num (int): The number to be placed in the cell.

        Returns:
            bool: True if the move is valid, False otherwise.

        This method checks whether placing the specified number in the given
        row violates the rules of Sudoku.
        """
        return num not in self.board[row]

    def _is_valid_col(self, col, num):
        """
        Check if placing a number in a specific column is a valid move.

        Args:
            col (int): The column index of the cell.
            num (int): The number to be placed in the cell.

        Returns:
            bool: True if the move is valid, False otherwise.

        This method checks whether placing the specified number in the given
        column violates the rules of Sudoku.
        """
        return num not in [self.board[row][col] for row in range(10)]

    def _is_valid_subgrid(self, row, col, num):
        """
        Check if placing a number in a specific subgrid is a valid move.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            num (int): The number to be placed in the cell.

        Returns:
            bool: True if the move is valid, False otherwise.

        This method checks whether placing the specified number in the given
        subgrid (3x3) violates the rules of Sudoku.
        """
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def _find_empty_cell(self, empty_cell):
        """
        Find the first empty cell in the Sudoku board.

        Args:
            empty_cell (tuple): A tuple to store the coordinates of the empty cell.

        Returns:
            bool: True if an empty cell is found, False otherwise.

        This method searches for the first empty cell in the Sudoku board and
        stores its coordinates in the provided tuple.
        """
        for row in range(10):
            for col in range(10):
                if self.board[row][col] == 0:
                    empty_cell = (row, col)
                    return True
        return False