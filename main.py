import pygame
import random
import copy
import pprint

class Board:

    # создание поля
    def __init__(self, width, height, screen, Font):
        self.width = width
        self.height = height
        self.clickedFlag = False
        self.prev_clickedFlag = False
        self.curr_column = -2
        self.curr_row = -2
        self.prev_column = -2
        self.prev_row = -2
        self.board = [[-1] * width for _ in range(height)]
        self.board_of_available_cells = []
        self.path_board = [[0] * width for _ in range(height)]
        row, column = 0, 0
        for i in self.board:
            row += 1
            for k in i:
                column += 1
                self.board_of_available_cells.append([row, column, k])
            column = 0
        # значения по умолчанию
        self.left = 175
        self.top = 100
        self.cell_size = 50
        self.cell_color = (245, 245, 245)
        self.frame_color = (255, 255, 255)
        self.frame_size = 2
        self.clicked_cell_color = (200, 200, 200)
        self.action_allowed = True
        self.color_dict = {1:(220, 0, 0), # 1 - Красный
                           2:(0, 0, 220), # 2 - Синий
                           3:(0, 220, 0), # 3 - Зеленый
                           4:(250, 250, 0), # 4 - Желтый
                           5:(220, 0, 220), # 5 - Фиолетовый
                           6:(0, 220, 220), # 6 - Голубой
                           7:(255, 165, 0)} # 7 - Оранжевый
        self.ball_radius = 20
        self.generated_balls = []
        self.screen = screen
        self.Font = Font
        self.score = 0
        for _ in range(3):
            self.generated_balls.append(random.choice([1, 2, 3, 4, 5, 6, 7]))

    # обновляет доску и рисует новые шары
    def update_board(self, screen):
        count_row = 0
        count_column = 0
        self.update_second_board()
        for i in self.board:
            count_row += 1
            for k in i:
                count_column += 1
                if k > 0:
                    pygame.draw.circle(screen, self.color_dict[k], (self.left + count_column * self.cell_size - self.cell_size // 2,
                                                                    self.top + count_row * self.cell_size - self.cell_size // 2), self.ball_radius, 20)
                    pygame.draw.circle(screen, (0, 0, 0),
                                       (self.left + count_column * self.cell_size - self.cell_size // 2,
                                        self.top + count_row * self.cell_size - self.cell_size // 2), self.ball_radius,
                                       2)

            count_column = 0
    # обновляет остальные доски (доски пути и свободных клеток)
    def update_second_board(self):
        row, column = 0, 0
        self.board_of_available_cells.clear()
        for i in self.board:
            row += 1
            for k in i:
                column += 1
                if k <= 0:
                    self.board_of_available_cells.append([row, column, k])
                    self.path_board[row - 1][column - 1] = 0
                else: self.path_board[row - 1][column - 1] = -1
            column = 0

    # начало хода
    def gamemove(self, screen):
        self.clickedFlag = False
        self.prev_clickedFlag = False
        self.prev_column = 0
        self.prev_row = 0
        self.fill_cell(self.curr_row, self.curr_column, self.cell_color)
        self.new_balls()
        self.update_board(screen)

    # проверяет, будет ли схлопывание шаров вокруг данного, и схлопывает, если будет, подсчитывает очки
    def check_ball(self, row, column):
        diagonal_1 = []
        diagonal_2 = []
        vertical = []
        horizontal = []
        for i in [(1, 1, diagonal_1),
                  (-1, -1, diagonal_1),
                  (-1, 1, diagonal_2),
                  (1, -1, diagonal_2),
                  (0, 1, horizontal),
                  (0, -1, horizontal),
                  (1, 0, vertical),
                  (-1, 0, vertical)]:
            curr_row = row
            curr_column = column
            while True:
                curr_row += i[0]
                curr_column += i[1]
                if not (0 < curr_row < 10 and 0 < curr_column < 10): break
                if self.board[curr_row - 1][curr_column - 1] != self.board[row - 1][column - 1]: break
                i[2].append((curr_row, curr_column))
        for i in (diagonal_1, diagonal_2, vertical, horizontal):
            if len(i) >= 4:
                for k in i:
                    self.board[k[0] - 1][k[1] - 1] = 0
                    self.fill_cell(*k, self.cell_color)
                self.board[row - 1][column - 1] = 0
                self.fill_cell(row, column, self.cell_color)
                self.score += (len(i) + 1) * (2 + len(i) - 5)
        pygame.draw.polygon(self.screen, (100, 100, 100), [(500, 20), (500, 50), (800, 50), (800, 20)])
        a = self.Font.render(f'Score: {self.score}', 1, (255, 255, 255))
        screen.blit(a, (500, 20))
        self.update_second_board()

    # генерация шаров (есть проблема генерации одинаковых шаров из-за особенностей псевдорандома)
    def new_balls(self):
        list_1 = []
        for i in self.generated_balls:
            try:
                row, column, color = random.choice(self.board_of_available_cells)
                self.board[row - 1][column - 1] = i
                list_1.append((row, column))
                self.update_second_board()
            except IndexError:
                self.end_of_game()
                pass
        for i in list_1:
            self.check_ball(i[0], i[1])
        self.generated_balls.clear()
        for _ in range(3):
            self.generated_balls.append(random.choice([1, 2, 3, 4, 5, 6, 7]))

        if self.board_of_available_cells == []:
            self.end_of_game()
            pass
        for i in [4, 5, 6]:
            pygame.draw.circle(screen, self.color_dict[self.generated_balls[i - 4]],
                               (self.left + i * self.cell_size - self.cell_size // 2,
                                self.cell_size // 2), self.ball_radius, 20)

            pygame.draw.circle(screen, (0, 0, 0),
                               (self.left + i * self.cell_size - self.cell_size // 2,
                                self.cell_size // 2), self.ball_radius,
                               2)

    # распространение волны
    def wave(self, row, column):
        cells = []
        curr_level = self.path_board[row - 1][column - 1]
        if row != 1 and self.path_board[row - 2][column - 1] == 0: cells.append((row - 1, column))
        if row != 9 and self.path_board[row][column - 1] == 0: cells.append((row + 1, column))
        if column != 9 and self.path_board[row - 1][column] == 0: cells.append((row, column + 1))
        if column != 1 and self.path_board[row - 1][column - 2] == 0: cells.append((row, column - 1))
        for i in cells:
            self.path_board[i[0] - 1][i[1] - 1] = curr_level + 1
        return cells

    # нахождение пути
    def path_find(self, row, column):
        cells = [(row, column)]
        curr_row, curr_column = row, column
        curr_level = self.path_board[row - 1][column - 1]
        for i in range(curr_level, 1, -1):
            if curr_row != 1 and self.path_board[curr_row - 2][curr_column - 1] == i - 1: cells.append((curr_row - 1, curr_column))
            elif curr_row != 9 and self.path_board[curr_row][curr_column - 1] == i - 1: cells.append((curr_row + 1, curr_column))
            elif curr_column != 9 and self.path_board[curr_row - 1][curr_column] == i - 1: cells.append((curr_row, curr_column + 1))
            elif curr_column != 1 and self.path_board[curr_row - 1][curr_column - 2] == i - 1: cells.append((curr_row, curr_column - 1))
            curr_row, curr_column = cells[-1]
        cells.pop(-1)
        return cells

    # настройка внешнего вида
    def set_view(self, left, top, cell_size, frame_size, frame_color, cell_color, ball_radius):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.frame_size = frame_size
        self.cell_color = cell_color
        self.frame_color = frame_color
        self.ball_radius = ball_radius

    # обработка клика
    def get_click(self, mouse_pos):
        if self.action_allowed:
            self.get_cell(mouse_pos)
            self.on_click()

    # очищает клетку (инструментальная функция)
    def fill_cell(self, row, column, color):
        pygame.draw.polygon(screen, color, [
            (self.left + (column - 1) * self.cell_size + 4,
             self.top + (row - 1) * self.cell_size + 4),
            (
                self.left + (column - 1) * self.cell_size + 4,
                self.top + row * self.cell_size - 4),
            (self.left + column * self.cell_size - 4, self.top + row * self.cell_size - 4),
            (self.left + column * self.cell_size - 4,
             self.top + (row - 1) * self.cell_size + 4)])

    # действия с клеткой, на которую кликнули
    def on_click(self):
        # отрисовка выбранной клетки и закрашивание предыдущей
        self.prev_clickedFlag = self.clickedFlag
        if 1 <= self.prev_column <= 9 and 1 <= self.prev_row <= 9: self.fill_cell(self.prev_row, self.prev_column, self.cell_color)
        if 1 <= self.curr_column <= 9 and 1 <= self.curr_row <= 9:
            if [self.prev_row, self.prev_column] == [self.curr_row, self.curr_column]:
                if self.clickedFlag:
                    self.clickedFlag = False

                else: self.clickedFlag = True

            else:
                self.clickedFlag = True

            if self.clickedFlag:
                pygame.draw.polygon(screen, self.clicked_cell_color, [
                    (self.left + (self.curr_column - 1) * self.cell_size + 4,
                     self.top + (self.curr_row - 1) * self.cell_size + 4),
                    (
                    self.left + (self.curr_column - 1) * self.cell_size + 4, self.top + self.curr_row * self.cell_size - 4),
                    (self.left + self.curr_column * self.cell_size - 4, self.top + self.curr_row * self.cell_size - 4),
                    (self.left + self.curr_column * self.cell_size - 4,
                     self.top + (self.curr_row - 1) * self.cell_size + 4)])
        else:
            self.clickedFlag = False
        self.update_board(self.screen)
        if 1 <= self.curr_column <= 9 and 1 <= self.curr_row <= 9:
            if 1 <= self.prev_column <= 9 and 1 <= self.prev_row <= 9:
                if (self.board[self.prev_row - 1][self.prev_column - 1] > 0
                        and self.board[self.curr_row - 1][self.curr_column - 1] <= 0
                        and self.clickedFlag
                        and self.prev_clickedFlag):
                    list_1 = [(self.prev_row, self.prev_column)]
                    list_2 = []
                    self.path_board[self.prev_row - 1][self.prev_column - 1] = 1
                    while list_1 != [] and self.path_board[self.curr_row - 1][self.curr_column - 1] == 0:
                        for i in list_1: list_2 += self.wave(*i)
                        list_1 = copy.deepcopy(list_2)
                        list_2 = []
                    if self.path_board[self.curr_row - 1][self.curr_column - 1] > 0:
                        cells = self.path_find(self.curr_row, self.curr_column)
                        prev_row, prev_column = self.prev_row, self.prev_column
                        for i in cells[::-1]:
                            self.board[i[0] - 1][i[1] - 1] = copy.copy(self.board[prev_row - 1][prev_column - 1])
                            self.board[prev_row - 1][prev_column - 1] = 0
                            self.fill_cell(prev_row, prev_column, self.cell_color)
                            if (prev_row, prev_column) == (self.prev_row, self.prev_column):
                                self.fill_cell(prev_row, prev_column, self.clicked_cell_color)
                                self.fill_cell(self.curr_row, self.curr_column, (0, 255, 0))
                            prev_row, prev_column = i[0], i[1] # добавить анимацию
                            self.update_board(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(300)
                        self.fill_cell(self.prev_row, self.prev_column, self.cell_color)
                        self.check_ball(self.curr_row, self.curr_column)
                        if self.board[self.curr_row - 1][self.curr_column - 1] > 0: self.gamemove(screen)

    # получение клетки по клику мышки
    def get_cell(self, mouse_pos):
        self.prev_column = self.curr_column
        self.prev_row = self.curr_row
        self.curr_column = ((mouse_pos[0] - self.left) // self.cell_size) + 1
        self.curr_row = ((mouse_pos[1] - self.top) // self.cell_size) + 1

    # отрисовка поля
    def render(self, screen, Font):
        count_column = 0
        count_row = 0
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
             self.left - 1,
             self.top - 1,
             self.width * self.cell_size + 3,
             self.width * self.cell_size + 3), 1)
        a = Font.render("Next:", 1, (255, 255, 255))
        screen.blit(a, (250, 20))
        # отрисовка клеток
        for i in range(self.height):
            count_row += 1
            for k in range(self.width):
                count_column += 1
                pygame.draw.polygon(screen, self.cell_color, [
                        (self.left + (count_column - 1) * self.cell_size, self.top + (count_row - 1) * self.cell_size),
                        (self.left + (count_column - 1) * self.cell_size, self.top + count_row * self.cell_size),
                        (self.left + count_column * self.cell_size, self.top + count_row * self.cell_size),
                        (self.left + count_column * self.cell_size, self.top + (count_row - 1) * self.cell_size)])

                pygame.draw.rect(screen, self.frame_color,
                                 pygame.Rect(self.left + (count_column - 1) * self.cell_size + 2,
                                             self.top + (count_row - 1) * self.cell_size + 2,
                                             self.cell_size - 3,
                                             self.cell_size - 3), self.frame_size)

                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.left + (count_column - 1) * self.cell_size,
                                                                       self.top + (count_row - 1) * self.cell_size,
                                                                       self.cell_size + 1,
                                                                       self.cell_size + 1), self.frame_size)

            count_column = 0
        for i in [3, 4, 5]:
            pygame.draw.polygon(screen, self.cell_color, [
                (self.left + i * self.cell_size, 0),
                (self.left + i * self.cell_size, self.cell_size),
                (self.left + (i + 1) * self.cell_size, self.cell_size),
                (self.left + (i + 1) * self.cell_size, 0)])

            pygame.draw.rect(screen, self.frame_color,
                             pygame.Rect(self.left + i * self.cell_size + 2,
                                         0,
                                         self.cell_size - 3,
                                         self.cell_size - 3), self.frame_size)

            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.left + i * self.cell_size,
                                                            0,
                                                            self.cell_size + 1,
                                                            self.cell_size + 1), self.frame_size)

    def end_of_game(self):
        global running
        running = False


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    pygame.display.set_caption("Color Lines")
    pygame.font.init()
    path = pygame.font.match_font("nunito")
    Font = pygame.font.Font(path, 30)
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    # основной цикл
    run = True
    while run:
        screen.fill((100, 100, 100))
        board = Board(9, 9, screen, Font)
        board.render(screen, Font)
        board.gamemove(screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
            pygame.display.flip()
    # завершение работы
    pygame.quit()