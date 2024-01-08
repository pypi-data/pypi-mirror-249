# sudoku_board.py
"""
Module for managing the Sudoku board.

This module includes the SudokuBoard class, which is responsible for managing
the game board, generating Sudoku puzzles, and checking the validity of moves.
"""
import random

class SudokuBoard:
   """
    Class for managing the Sudoku board.

    Attributes:
        board (list): A 10x10 grid representing the Sudoku board.
    """
    
    def __init__(self):
        """
        Initialize an empty Sudoku board.

        The board is represented as a 10x10 grid, where each cell can contain
        a number from 0 to 9. A value of 0 indicates an empty cell.
        """
        self.board = [[0] * 10 for _ in range(10)]

    def print_board(self):
        """
        Print the current state of the Sudoku board.

        The board is printed as a grid, displaying each row on a separate line.
        """
        for row in self.board:
            print(" ".join(map(str, row)))        

    def place_number(self, row, col, num):
        """
        Place a number in a specific cell of the Sudoku board.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            num (int): The number to be placed in the cell.

        Returns:
            bool: True if the placement is successful, False otherwise.

        This method attempts to place the specified number in the given cell.
        If the move is valid, the number is placed, and True is returned.
        Otherwise, the board remains unchanged, and False is returned.
        """
        if self.is_valid_move(row, col, num):
            self.board[row][col] = num
            return True
        return False
    
    def is_board_full(self):
        """
        Check if the Sudoku board is completely filled.

        Returns:
            bool: True if the board is fully filled, False otherwise.

        This method checks whether all cells in the Sudoku board are filled
        with non-zero numbers, indicating that the board is complete.
        """
        return all(all(cell != 0 for cell in row) for row in self.board)
    
    def generate_board(self, difficulty):
        """
        Generate a Sudoku board with the specified difficulty level.

        Args:
            difficulty (int): The difficulty level, indicating the number of
                             initially empty cells.

        This method generates a random Sudoku board using a backtracking
        algorithm and then removes numbers to achieve the desired difficulty.
        """
        self._generate_board()
        self._remove_numbers(difficulty)

    def _generate_board(self):
        """
        Generate a random Sudoku solution using backtracking.

        Returns:
            bool: True if a solution is found, False otherwise.

        This method is used internally to generate a random solution for the
        Sudoku board using a backtracking algorithm.
        """
        empty_cell = (0, 0)
        if not self._find_empty_cell(empty_cell):
            return True

        row, col = empty_cell
        numbers = list(range(1, 11))
        random.shuffle(numbers)

        for num in numbers:
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                if self._generate_board():
                    return True
                self.board[row][col] = 0

        return False

    def _remove_numbers(self, difficulty):
        """
        Remove numbers from the board to achieve the desired difficulty.

        Args:
            difficulty (int): The desired difficulty level, indicating the
                             number of initially empty cells.

        This method removes numbers from the generated Sudoku board to achieve
        the specified difficulty level while ensuring a unique solution.
        """
        cells = [(row, col) for row in range(10) for col in range(10)]
        random.shuffle(cells)

        for cell in cells:
            row, col = cell
            temp = self.board[row][col]
            self.board[row][col] = 0

            # Check if the board still has a unique solution
            if not self._has_unique_solution():
                self.board[row][col] = temp

            # Check if the desired difficulty level is reached
            if self._count_empty_cells() >= difficulty:
                break

    def _has_unique_solution(self):
        """
        Check if the current Sudoku board has a unique solution.

        Returns:
            bool: True if the board has a unique solution, False otherwise.

        This method checks whether the current Sudoku board has a unique
        solution by attempting to solve it and counting the number of
        solutions.
        """
        original_board = [row[:] for row in self.board]
        solver = SudokuSolver(self.board)
        solver.solve()
        return solver.is_unique_solution(original_board)

    def _count_empty_cells(self):
        """
        Count the number of empty cells in the Sudoku board.

        Returns:
            int: The number of empty cells in the board.

        This method counts the number of cells in the Sudoku board that are
        still empty (filled with zero).
        """
        return sum(row.count(0) for row in self.board)

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