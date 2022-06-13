from simplex import SimplexSolver
from fractions import Fraction


class MatrixGameSolver:

    def __init__(self):
        self.matrix = []
        self.first_b_matrix = []
        self.first_c_matrix = []
        self.second_b_matrix = []
        self.second_c_matrix = []
        self.saddle_point = {}
        self.first_player_strategy = {}
        self.second_player_strategy = {}
        self.second_ineq = []

    def run_matrix_game_solver(self):
        self.create_matrices()
        self.get_matrix_saddle_point()

        if self.saddle_point['exist']:
            self.first_player_strategy[self.saddle_point['coordinates']['row']] = 1
            self.second_player_strategy[self.saddle_point['coordinates']['column']] = 1

            print('Сідловою точкою є пара i = {}'.format(self.saddle_point['coordinates']['row']),
                  '; та j = {}'.format(self.saddle_point['coordinates']['column']),
                  '; при якій V = {}'.format(self.saddle_point['value']), sep='')
            print('Дана матриця має розв`язок в чистих стратегіях', end='\n')
            print('Стратегія для першого гравця:')
            print(self.first_player_strategy)
            print('Стратегія для другого гравця:')
            print(self.second_player_strategy)

        if not(self.saddle_point['exist']):
            matrix_transpose = []
            for i in range(len(self.matrix[0])):
                matrix_transpose.append(self.get_matrix_column(self.matrix, i))
            first_player_simplex = SimplexSolver().run_simplex(matrix_transpose,
                                                               self.second_b_matrix,
                                                               self.second_c_matrix, 'min', self.second_ineq)
            self.first_player_strategy = self.get_player_strategy(first_player_simplex, 'y')
            print("Оптимальна стратегія для першого гравця:")
            print(self.first_player_strategy)
            print("\n")
            input("Натисніть enter щоб продовжити...")

            second_player_simplex = SimplexSolver().run_simplex(self.matrix,
                                                                self.first_b_matrix,
                                                                self.first_c_matrix)
            self.second_player_strategy = self.get_player_strategy(second_player_simplex, 'x')
            print("Оптимальна стратегія для другого гравця:")
            print(self.second_player_strategy)

    def create_matrices(self):

        rows = int(input("Введіть кількість рядків: "))
        for i in range(rows):
            row = list(map(int, input().split()))
            self.matrix.append(row)

        column_number = len(self.matrix[0])

        self.first_b_matrix = [1] * rows
        self.first_c_matrix = [1] * column_number
        self.second_b_matrix = [1] * column_number
        self.second_c_matrix = [1] * rows
        self.second_ineq = ['>='] * column_number

        self.first_player_strategy = [0] * rows
        self.second_player_strategy = [0] * column_number

    def get_matrix_saddle_point(self):
        V_t = None
        V_b = None
        matrix_width = len(self.matrix[0])
        matrix_transpose = []
        saddle_point_row = 0
        saddle_point_column = 0

        i = 0
        for row in self.matrix:
            min_element = row[0]
            for element in row:
                min_element = element if element < min_element else min_element
            if V_t is None:
                V_t = min_element
                saddle_point_column = i if min_element > V_t else saddle_point_column
            else:
                V_t = min_element if min_element > V_t else V_t
                saddle_point_column = i if min_element > V_t else saddle_point_column
            i += 1

        for i in range(matrix_width):
            matrix_transpose.append(self.get_matrix_column(self.matrix, i))

        i = 0
        for row in matrix_transpose:
            max_element = row[0]
            for element in row:
                max_element = element if element > max_element else max_element
            if V_b is None:
                V_b = max_element
                saddle_point_row = i if max_element > V_t else saddle_point_row
            else:
                V_b = max_element if max_element < V_b else V_b
                saddle_point_row = i if max_element > V_t else saddle_point_row
            i += 1
        if V_t == V_b:
            self.saddle_point['exist'] = True
            self.saddle_point['coordinates'] = {}
            self.saddle_point['coordinates']['row'] = saddle_point_row
            self.saddle_point['coordinates']['column'] = saddle_point_column
            self.saddle_point['value'] = V_t
        else:
            self.saddle_point['exist'] = False
            self.saddle_point['v_bottom'] = V_b
            self.saddle_point['v_top'] = V_t

    def get_matrix_column(self, curr_matrix, i):
        return [row[i] for row in curr_matrix]

    def get_player_strategy(self, simplex_solution, variables):
        player_strategy = {}
        sum = 0
        for key, value in simplex_solution.items():
            if key.startswith(variables):
                sum += value
        for key, value in simplex_solution.items():
            if key.startswith(variables):
                player_strategy[key] = float(value) / sum

        return player_strategy

def main():
    game_solver = MatrixGameSolver()
    game_solver.run_matrix_game_solver()


if __name__ == "__main__":
    main()
