def _is_valid_move(self, row, col, num):
        """
        Check if placing a number in a specific cell is a valid move.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            num (int): The number to be placed in the cell.

        Returns:
            bool: True if the move is valid, False otherwise.

        This method checks whether placing the specified number in the given
        cell violates the rules of Sudoku. It checks for conflicts in the
        current row, column, and subgrid.
        """
        return (
            self._is_valid_row(row, num) and
            self._is_valid_col(col, num) and
            self._is_valid_subgrid(row, col, num)
        )