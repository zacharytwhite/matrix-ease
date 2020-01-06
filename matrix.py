"""Module to assist in the handling of matrices.

This module offers basic matrices operations, namely addition,
subtraction, multiplication, and inverse.
"""

__version__ = '0.1'

import copy
import math
# from fractions import Fraction


def display_matrix(matrix: list):
    if Matrix.is__matrix(matrix):
        for row in matrix:
            print(row)
    else:
        print('Input is not a matrix, but here it is anyways:')
        print(matrix)


class Matrix:
    def __init__(self, matrix: list):
        if Matrix.is__matrix(matrix):
            self.__matrix = matrix
        else:
            raise TypeError('Expected a matrix (2-dimensional list) - '
                            f'instead was given {type(matrix).__name__}.')

    def get__matrix(self):
        return self.__matrix

    def set__matrix(self, new__matrix: list):
        if Matrix.is__matrix(new__matrix):
            self.__matrix = new__matrix


    @classmethod
    def is__matrix(cls, matrix: list):
        """Determines if matrix is a valid matrix."""
        if not matrix: return False
        if isinstance(matrix, Matrix): return True
        if (type(matrix) != list or type(matrix[0]) != list): return False

        length = len(matrix[0])
        if not matrix or not all(len(row) == length for row in matrix):
            return False
        
        return True

    @classmethod
    def is_identity(cls, matrix: list):
        """Determines if matrix is an identity matrix.
        
        A matrix is an identity matrix if
        it meets the following criteria:
            1: It must be "square" (i.e. have the same number of
               rows as columns),
            2: It must have 1s along its diagonal (starting in the
               top-left corner) and 0s everywhere else.
        """
        rows = len(matrix)
        columns = len(matrix[0])

        if not Matrix.is__matrix(matrix) or rows != columns: return False

        # Flatten the array.
        flat = [item for sublist in matrix for item in sublist]
        
        for i in range(0, (rows*columns+1), (rows+1)):
            if flat[i] != 1:
                return False
            if flat[i] == 1:
                flat[i] = 0

        return False if not all(num == 0 for num in flat) else True


    def add(self, addend: list):
        """Adds provided matrix to self."""
        result = []
        if not Matrix.is__matrix(addend): return result
        
        # Height and width of self and addend.
        rows_a = len(self.__matrix)
        columns_a = len(self.__matrix[0])
        rows_b = len(addend)
        columns_b = len(addend[0])

        if rows_a != rows_b or columns_a != columns_b: return result

        for i in range(0, rows_a):
            new_row = []
            for j in range(0, columns_a):
                new_row.append(self.__matrix[i][j] + addend[i][j])

            result.append(new_row)

        return result

    def subtract(self, subtrahend: list):
        """Subtracts provided matrix from self."""
        result = []
        if not Matrix.is__matrix(subtrahend): return result

        # Height and width of self and subtrahend.
        rows_a = len(self.__matrix)
        columns_a = len(self.__matrix[0])
        rows_b = len(subtrahend)
        columns_b = len(subtrahend[0])

        if rows_a != rows_b or columns_a != columns_b: return result

        for i in range(0, rows_a):
            new_row = []
            for j in range(0, columns_a):
                new_row.append(self.__matrix[i][j] - subtrahend[i][j])
            result.append(new_row)

        return result

    def multiply(self, multiplier):
        """Multiplies self by matrix or scalar, depending on param."""
        result = []

        if isinstance(multiplier, list):
            if not Matrix.is__matrix(multiplier): return result

            # Height and width of self and multiplier.
            rows_a = len(self.__matrix)
            columns_a = len(self.__matrix[0])
            rows_b = len(multiplier)
            columns_b = len(multiplier[0])
            # Ensure matrices have complimentary dimensions.
            if rows_a != columns_b or columns_a != rows_b: return result

            for i in range(0, rows_a):
                new_row = []
                for j in range(0, columns_b):
                    dot_product = 0
                    for k in range(columns_a):
                        dot_product += self.__matrix[i][k] * multiplier[k][j]
                    new_row.append(dot_product)
                result.append(new_row)

        elif isinstance(multiplier, int):
            rows = len(self.__matrix)
            columns = len(self.__matrix[0])

            for i in range(0, rows):
                new_row = []
                for j in range(0, columns):
                    new_row.append(self.__matrix[i][j] * multiplier)
                result.append(new_row)

        return result


    @classmethod
    def delete_row_and_column(cls, matrix: list, row: int, column: int=-1):
        """Returns copy of matrix with indexed row & column removed."""
        # Create copy of matrix to avoid mutating the original.
        temp = copy.deepcopy(matrix)
        
        if column != -1:
            temp.pop(row)
            for i in range(0, len(temp)):
                temp[i].pop(column)
        else:
            del temp[0]
            for i in range(0, len(temp)):
                del temp[i][row]
        return temp

    @classmethod
    def determinant(cls, matrix: list):
        if not Matrix.is__matrix(matrix): return

        rows = len(matrix)
        columns = len(matrix[0])
        if rows != columns: return
        
        if rows == 2:
            return (matrix[0][0] * matrix[1][1] -
                matrix[0][1] * matrix[1][0])
        else:
            result = 0
            for i in range(0, rows):
                result += (((-1)**i) * matrix[0][i] * Matrix.determinant(
                    Matrix.delete_row_and_column(matrix, i)))
        return result

    def cofactors(self):
        """Creates a matrix of cofactors of a matrix."""
        rows = len(self.__matrix)
        columns = len(self.__matrix[0])
        if rows != columns: return

        result = []
        for i in range (0, rows):
            new_row = []
            for j in range(0, columns):
                d = (((-1)**((i)+(j)) * Matrix.determinant(
                    Matrix.delete_row_and_column(self.__matrix, i, j))))
                new_row.append(d)
            result.append(new_row)
        return result

    def adjugate(self):
        """Transposes elements of matrix across the diagonal."""
        result = []
        result_rows = len(self.__matrix[0])
        result_columns = len(self.__matrix)

        for i in range(0, result_rows):
            new_row = []
            for j in range(0, result_columns):
                new_row.append(self.__matrix[j][i])
            result.append(new_row)
        return result

    def inverse(self):
        """Determines the inverse of a matrix (if it exists)."""
        rows = len(self.__matrix)
        columns = len(self.__matrix[0])
        if rows != columns: return

        determinant = Matrix.determinant(self.__matrix)
        # If a matrix's determinant is 0, it is not invertible.
        if determinant == 0: return

        cofactors = self.cofactors()
        adjugate = self.adjugate()
        inverse = []

        for i in range(rows):
            new_row = []
            for j in range(columns):
                # fraction = Fraction(cofactors[i][j], determinant)
                # new_row.append([fraction.numerator, fraction.denominator])
                new_row.append(round((1.0/determinant * cofactors[i][j]), 3))
            inverse.append(new_row)
        
        return inverse


    @staticmethod
    def create__matrix(array: list, rows: int, columns: int):
        if rows * columns != len(array):
            print('Error — provided dimensions would result'
                  'in invalid matrix.')
            return

        matrix = []
        for i in range(0, len(array), columns):
            matrix.append(array[i:i+columns])

        return matrix

    @staticmethod
    def create__matrix_from_user():
        """Creates a matrix from user input."""
        number_of_rows = input('How many rows should your matrix have? ')
        
        array = []
        for i in range(0, int(number_of_rows)):
            raw_row = input(f'Enter the values for row {i+1} —— '
                'seperate each element by a single space:\n').strip()
            elements = raw_row.split(' ')

            try:
                row = [int(el) for el in elements]
            except ValueError as e:
                print('\nError: expected integer(s).\n')
                return []
            else:
                array.append(row)
        print()
        return array if Matrix.is__matrix(array) else []


"""
Example matrices:

m_3_3 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

m_id = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]

m_3_2 = [
    [1, 4],
    [2, 5],
    [3, 6],
]

m_2_3 = [
    [1, 2, 3],
    [4, 5, 6],
]

x = [
    [1, 3, 3],
    [4, 5, 6],
    [7, 8, 9],
  ]
"""
