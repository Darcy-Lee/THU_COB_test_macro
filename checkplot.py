import os
import numpy as np
import matplotlib.pyplot as plt

class ByteError:
    def __init__(self, line, column, subip):
        self.line = line
        self.column = column
        self.subip = subip

class ErrorMatrix:
    def __init__(self):
        self.errors = []

    def add_error(self, line, column, subip):
        self.errors.append(ByteError(line, column, subip))

    def generate_matrix(self):
        matrix = np.zeros((1179, 312 * 8), dtype=int)
        for error in self.errors:
            matrix[error.line, error.subip * 312 + error.column] = 1
        # flip the matrix vertically
        matrix = np.flipud(matrix)
        return matrix

def read_files_and_collect_errors():
    error_matrix = ErrorMatrix()
    for subip in range(8):
        filename = f'Pagedata\\RRAMpage_SUBIP{subip}.txt'
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines):
                bytes_values = line.split()
                for col_num, byte in enumerate(bytes_values):
                    # if byte not in {'00', 'FF'}:
                    if byte not in {'00'}:
                    # if byte not in {'FF'}:
                        error_matrix.add_error(line_num, col_num, subip)
    return error_matrix

def plot_error_matrix(matrix):
    plt.figure(figsize=(20, 20))
    # plt.imshow(matrix, cmap='gray_r', interpolation='none')  # 'gray_r' to reverse the colormap
    plt.imshow(matrix, interpolation='none')  # 'gray_r' to reverse the colormap


    # Draw vertical lines to separate SUBIPs
    for subip in range(1, 8):
        plt.axvline(x=subip * 312 - 0.5, color='blue', linestyle='-', linewidth=0.5)

    plt.title('Error Matrix')
    plt.show()

def main():
    error_matrix = read_files_and_collect_errors()
    matrix = error_matrix.generate_matrix()
    plot_error_matrix(matrix)

if __name__ == '__main__':
    main()
