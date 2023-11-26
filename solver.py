"""Основной модуль с решателем"""
from typing import List, Any


def solve(filename, order) -> list[float] | str:
    """Решатель принимает порядок и имя файла, для которого надо рассчитать коэффициенты МНК"""
    x, y = [], []
    points = set()
    with open('uploads/' + filename) as file:
        for i in file.readlines():
            xc, yc = int(i.split()[0]), int(i.split()[1])
            if (xc, yc) not in points:
                points.add((xc, yc))
                x.append(xc)
                y.append(yc)
    k = order + 1
    if k < 1:
        return "Ошибка, порядок должен быть больше"
    matrix = []
    for ki in range(k):
        matrix.append([])
        for kj in range(k):
            matrix[ki].append(sum([xi ** (ki + kj) for xi in x]))
    vector = []
    for kt in range(k):
        vector.append(sum([y[t] * x[t] ** kt for t in range(len(x))]))
    print(matrix, vector)
    try:
        return solve_gaussian_elimination(matrix, vector)
    except Exception:
        return "Ошибка, уравнение вырожденное"

# def determinant(matrix):
#     # Функция для вычисления определителя квадратной матрицы
#     n = len(matrix)
#     if n == 1:
#         return matrix[0][0]
#     elif n == 2:
#         return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
#     else:
#         det = 0
#         for j in range(n):
#             minor = [row[:j] + row[j+1:] for row in matrix[1:]]
#             det += matrix[0][j] * determinant(minor) * (-1) ** j
#         return det

def solve_gaussian_elimination(A, b):
    n = len(A)

    # Прямой ход метода Гаусса
    for i in range(n):
        # Поиск максимального элемента в столбце
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k

        # Обмен строками, чтобы максимальный элемент был на главной диагонали
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Приведение к диагональному виду
        pivot = A[i][i]
        if pivot == 0:
            raise Exception("Метод Гаусса не применим: деление на ноль")
        for j in range(i, n):
            A[i][j] /= pivot
        b[i] /= pivot

        for k in range(i + 1, n):
            factor = -A[k][i]
            for j in range(i, n):
                A[k][j] += factor * A[i][j]
            b[k] += factor * b[i]

    # Обратный ход метода Гаусса    
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]

    return x