import pygame
import random
import copy
import csv

from pygame.draw_py import draw_polygon

pygame.init()
path = pygame.font.match_font("nunito")
Font = pygame.font.Font(path, 30)
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Color Lines")
color = pygame.Color('white')

# Создаем объект Clock
clock = pygame.time.Clock()

def move_ball_animation(board, start_row, start_col, end_row, end_col, screen, clock):
    """Функция для анимации перемещения шарика"""

    # Координаты центра начальной клетки
    start_x = board.left + start_col * board.cell_size - board.cell_size // 2
    start_y = board.top + start_row * board.cell_size - board.cell_size // 2

    # Координаты центра конечной клетки
    end_x = board.left + end_col * board.cell_size - board.cell_size // 2
    end_y = board.top + end_row * board.cell_size - board.cell_size // 2

    # Количество кадров для анимации
    frames = 15

    # Шаг изменения координат за каждый кадр
    step_x = (end_x - start_x) / frames
    step_y = (end_y - start_y) / frames

    # Начальные координаты для анимации
    current_x, current_y = start_x, start_y

    # Цвет шара
    color = board.color_dict[board.board[start_row - 1][start_col - 1]]

    # Запускаем анимацию
    for _ in range(frames):
        # Чертим текущий кадр
        board.fill_cell(start_row, start_col, board.cell_color)
        board.fill_cell(end_row, end_col, board.cell_color)

        # Рисуем перемещающийся шарик

        pygame.draw.circle(screen, color, (int(current_x), int(current_y)), board.ball_radius, 0)
        pygame.draw.circle(screen, (0, 0, 0),
                           (int(current_x), int(current_y)), board.ball_radius,
                           2)

        # Обновляем экран
        pygame.display.flip()

        # Изменяем текущие координаты
        current_x += step_x
        current_y += step_y

        # Задержка перед следующим кадром
        clock.tick(60)

    # После завершения анимации обновляем доску
    board.board[end_row - 1][end_col - 1] = copy.copy(board.board[start_row - 1][start_col - 1])
    board.board[start_row - 1][start_col - 1] = 0


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
        self.left = 0
        row, column = 0, 0
        for i in self.board:
            row += 1
            for k in i:
                column += 1
                self.board_of_available_cells.append([row, column, k])
            column = 0
        # значения по умолчанию
        if self.width == 9:
            self.left = 175
        elif self.width == 5:
            self.left = 275
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
        self.dim = 5
        if self.width == 5:
            self.color_dict = {1:(220, 0, 0), # 1 - Красный
                               2:(0, 0, 220), # 2 - Синий
                               3:(0, 220, 0), # 3 - Зеленый
                               4:(250, 250, 0), # 4 - Желтый
                               5:(220, 0, 220), # 5 - Фиолетовый
                               6:(0, 220, 220), # 6 - Голубой
                               }
            self.dim = 3
        self.ball_radius = 20
        self.generated_balls = []
        self.screen = screen
        self.Font = Font
        self.score = 0
        for _ in range(3):
            self.generated_balls.append(random.choice(list(self.color_dict)))

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
    # обновляет остальные доски (доски пути и свободных клеток) 2
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
        self.action_allowed = True
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
                if not (0 < curr_row < self.height + 1 and 0 < curr_column < self.width + 1): break
                if self.board[curr_row - 1][curr_column - 1] != self.board[row - 1][column - 1]: break
                i[2].append((curr_row, curr_column))
        for i in (diagonal_1, diagonal_2, vertical, horizontal):
            if (len(i) >= 4 and self.width == 9) or (len(i) >= 3 and self.width == 5):
                for k in i:
                    self.board[k[0] - 1][k[1] - 1] = 0
                    self.fill_cell(*k, self.cell_color)
                self.board[row - 1][column - 1] = 0
                self.fill_cell(row, column, self.cell_color)
                self.score += (len(i) + 1) * (2 + len(i) - self.dim) * 13
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
            self.generated_balls.append(random.choice(list(self.color_dict)))

        if self.board_of_available_cells == []:
            self.end_of_game()
            pass
        for i in [4, 5, 6]:
            pygame.draw.circle(screen, self.color_dict[self.generated_balls[i - 4]],
                               (175 + i * self.cell_size - self.cell_size // 2,
                                self.cell_size // 2), self.ball_radius, 20)

            pygame.draw.circle(screen, (0, 0, 0),
                               (175 + i * self.cell_size - self.cell_size // 2,
                                self.cell_size // 2), self.ball_radius,
                               2)

    # распространение волны
    def wave(self, row, column):
        cells = []
        curr_level = self.path_board[row - 1][column - 1]
        if row != 1 and self.path_board[row - 2][column - 1] == 0: cells.append((row - 1, column))
        if row != self.height and self.path_board[row][column - 1] == 0: cells.append((row + 1, column))
        if column != self.width and self.path_board[row - 1][column] == 0: cells.append((row, column + 1))
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
            elif curr_row != self.height and self.path_board[curr_row][curr_column - 1] == i - 1: cells.append((curr_row + 1, curr_column))
            elif curr_column != self.width and self.path_board[curr_row - 1][curr_column] == i - 1: cells.append((curr_row, curr_column + 1))
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

    # очищает клетку (инструментальная функция)
    def fill_cell(self, count_row, count_column, color):
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

    # обработка клика
    def get_click(self, mouse_pos):
        if self.action_allowed:
            self.get_cell(mouse_pos)
            self.on_click()

    # действия с клеткой, на которую кликнули

    def on_click(self):
        # отрисовка выбранной клетки и закрашивание предыдущей
        self.prev_clickedFlag = self.clickedFlag
        if 1 <= self.prev_column <= self.width and 1 <= self.prev_row <= self.height: self.fill_cell(self.prev_row, self.prev_column, self.cell_color)
        if 1 <= self.curr_column <= self.width and 1 <= self.curr_row <= self.height:
            if [self.prev_row, self.prev_column] == [self.curr_row, self.curr_column]:
                if self.clickedFlag:
                    self.clickedFlag = False
                else:
                    self.clickedFlag = True
            else:
                self.clickedFlag = True
            if self.clickedFlag:
                pygame.draw.polygon(screen, self.clicked_cell_color, [
                    (self.left + (self.curr_column - 1) * self.cell_size + 4,
                     self.top + (self.curr_row - 1) * self.cell_size + 4),
                    (
                        self.left + (self.curr_column - 1) * self.cell_size + 4,
                        self.top + self.curr_row * self.cell_size - 4),
                    (self.left + self.curr_column * self.cell_size - 4, self.top + self.curr_row * self.cell_size - 4),
                    (self.left + self.curr_column * self.cell_size - 4,
                     self.top + (self.curr_row - 1) * self.cell_size + 4)])
        else:
            self.clickedFlag = False
        self.update_board(self.screen)
        if 1 <= self.curr_column <= self.width and 1 <= self.curr_row <= self.height:
            if 1 <= self.prev_column <= self.width and 1 <= self.prev_row <= self.height:
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
                        self.action_allowed = False
                        cells = self.path_find(self.curr_row, self.curr_column)
                        prev_row, prev_column = self.prev_row, self.prev_column
                        for i in cells[::-1]:
                            # Вызов функции анимации перемещения
                            move_ball_animation(self, prev_row, prev_column, i[0], i[1], screen, clock)

                            # Обновить данные после анимации
                            prev_row, prev_column = i[0], i[1]
                        self.fill_cell(self.prev_row, self.prev_column, self.cell_color)
                        self.check_ball(self.curr_row, self.curr_column)
                        self.action_allowed = True
                        if self.board[self.curr_row - 1][self.curr_column - 1] > 0: self.gamemove(screen)


    # получение клетки по клику мышки
    def get_cell(self, mouse_pos):
        self.prev_column = self.curr_column
        self.prev_row = self.curr_row
        self.curr_column = ((mouse_pos[0] - self.left) // self.cell_size) + 1
        self.curr_row = ((mouse_pos[1] - self.top) // self.cell_size) + 1

    # отрисовка поля
    def render(self, screen, Font):
        screen.fill((100, 100, 100))
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
                (175 + i * self.cell_size, 0),
                (175 + i * self.cell_size, self.cell_size),
                (175 + (i + 1) * self.cell_size, self.cell_size),
                (175 + (i + 1) * self.cell_size, 0)])

            pygame.draw.rect(screen, self.frame_color,
                             pygame.Rect(175 + i * self.cell_size + 2,
                                         0,
                                         self.cell_size - 3,
                                         self.cell_size - 3), self.frame_size)

            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(175 + i * self.cell_size,
                                                            0,
                                                            self.cell_size + 1,
                                                            self.cell_size + 1), self.frame_size)

    def end_of_game(self):
        global running
        if running:
            In = []
            with open('records.csv', encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for index, row in enumerate(reader):
                    In.append(row)
            csvfile.close()

            with open('records.csv', 'w', newline='', encoding="utf8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in In:
                    writer.writerow(i)
                writer.writerow(["You", self.width, self.score])
            csvfile.close()
        running = False


class Menu:

    def __init__(self, screen, Font, flag):
        self.flag = flag
        self.action_allowed = True
        self.middle = 20
        self.button_width = 150
        self.button_height = 40
        self.left = 325
        self.screen = screen
        self.font = Font
        self.button_color = (245, 245, 245)
        self.frame_color = (255, 255, 255)
        self.frame_size = 2
        self.clicked_cell_color = (200, 200, 200)
        self.curr_button_val = -1
        self.prev_button_val = -1
        self.past_button_val = -1

        In_5 = []
        In_9 = []
        with open('records.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for index, row in enumerate(reader):
                if index == 0:
                    In_5.append(row)
                    In_9.append(row)
                elif row[1] == "5":
                    In_5.append(row)
                else: In_9.append(row)
        self.In_5 = sorted(In_5, key=lambda x: x[2])
        self.In_9 = sorted(In_9, key=lambda x: x[2])
        csvfile.close()

        if flag == "Start":
            self.buttons = [[5, 9, "Back"],
                            [In_5, In_9, "Back"],
                            ["Back"]]
            self.result = "COLOR LINES"
            self.first_buttons = ["New game", "Records", "Options", "Exit"]
        else:
            self.result = f'GAME OVER!  Your score is: {board.score}'
            self.first_buttons = ["Main menu", "Exit"]
        self.Board_size = 0

    def get_click(self, mouse_pos):
        if self.action_allowed:
            self.get_button(mouse_pos)
            self.on_click()

    def get_button(self, mouse_pos):
        if self.left <= mouse_pos[0] <= 800 - self.left:
            self.curr_button_val = ((mouse_pos[1] - 110) // (self.button_height + self.middle)) + 1
            if 110 + self.curr_button_val * self.button_height + (self.curr_button_val - 1) * self.middle >= mouse_pos[1]:
                self.curr_button_val -= 1
            else:
                self.curr_button_val = -1

    def on_click(self):
        global menu_flag
        global menu_flag_2
        global run
        global running
        menu_flag, menu_flag_2, run, running = True, True, True, True
        if self.flag == "Start":
            if self.curr_button_val == -1 or self.curr_button_val > 3:
                if self.curr_button_val == 6 and self.prev_button_val in [0, 1] and self.past_button_val == 1:
                    self.curr_button_val = -1
                    self.prev_button_val = self.past_button_val
                    self.past_button_val = -1
                    self.render_new_menu("RECORDS", ["5 x 5", "9 x 9", "Back"])
            elif self.past_button_val == -1:
                if self.prev_button_val == -1:
                    self.prev_button_val = self.curr_button_val
                    if self.curr_button_val == 0: self.render_new_menu("NEW GAME", ["5 x 5", "9 x 9", "Back"])
                    elif self.curr_button_val == 1: self.render_new_menu("RECORDS", ["5 x 5", "9 x 9", "Back"])
                    elif self.curr_button_val == 2: self.render_new_menu("OPTIONS", ["Back"])
                    elif self.curr_button_val == 3:
                        run, running, menu_flag, menu_flag_2 = False, False, False, False
                elif self.prev_button_val == 1 and self.curr_button_val in [0, 1] and self.past_button_val == -1:
                    self.past_button_val = self.prev_button_val
                    self.prev_button_val = self.curr_button_val
                    self.render_records_menu(self.buttons[1][self.curr_button_val])
                elif 0 <= self.curr_button_val <= len(self.buttons[self.prev_button_val]) - 1:
                    if self.buttons[self.prev_button_val][self.curr_button_val] == "Back":
                        self.prev_button_val = -1
                        self.curr_button_val = -1
                        self.render_menu(self.screen)
                    elif self.curr_button_val != -1 and self.prev_button_val != -1:
                        if self.prev_button_val == 0:
                            menu_flag = False
                            self.Board_size = self.buttons[self.prev_button_val][self.curr_button_val]
                            pass
                        elif self.prev_button_val == 1:
                            self.render_records_menu(self.buttons[self.prev_button_val][self.curr_button_val])
                        else: pass
        else:
            if self.curr_button_val == -1: pass
            elif self.curr_button_val == 1:
                run, running, menu_flag, menu_flag_2 = False, False, False, False
                pass
            elif self.curr_button_val == 0:
                menu_flag_2 = False
                pass

    def render_menu(self, screen):
        screen.fill((100, 100, 100))
        a = self.font.render(self.result, 1, (255, 255, 255))
        text_rect = a.get_rect(center=(800 / 2, 50))
        screen.blit(a, text_rect)
        c = 1
        for i in self.first_buttons:
            c += 1
            pygame.draw.polygon(screen, self.button_color, [
                (self.left, (c - 1) * self.middle + (c - 1) * self.button_height + 50),
                (self.left, (c - 1) * self.middle + c * self.button_height + 50),
                (self.left + self.button_width, (c - 1) * self.middle + c * self.button_height + 50),
                (self.left + self.button_width, (c - 1) * self.middle + (c - 1) * self.button_height + 50)])
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.left,
                                                                    (c - 1) * self.middle + (c - 1) * self.button_height + 50,
                                                                    self.button_width + 1,
                                                                    self.button_height + 1), 1)
            pygame.draw.rect(screen, self.frame_color, pygame.Rect(self.left + 2,
                                                            (c - 1) * self.middle + (c - 1) * self.button_height + 50 + 2,
                                                            self.button_width - 2,
                                                            self.button_height - 2), 1)
            a = self.font.render(i, 1, (10, 10, 10))
            text_rect = a.get_rect(center=(800 / 2, c * (self.middle + self.button_height) + 10))
            screen.blit(a, text_rect)

    def render_new_menu(self, heading, list_1):
        screen = self.screen
        screen.fill((100, 100, 100))
        a = self.font.render(heading, 1, (255, 255, 255))
        text_rect = a.get_rect(center=(800 / 2, 50))
        screen.blit(a, text_rect)
        c = 1
        for i in list_1:
            c += 1
            pygame.draw.polygon(screen, self.button_color, [
                (self.left, (c - 1) * self.middle + (c - 1) * self.button_height + 50),
                (self.left, (c - 1) * self.middle + c * self.button_height + 50),
                (self.left + self.button_width, (c - 1) * self.middle + c * self.button_height + 50),
                (self.left + self.button_width, (c - 1) * self.middle + (c - 1) * self.button_height + 50)])
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.left,
                                                            (c - 1) * self.middle + (c - 1) * self.button_height + 50,
                                                            self.button_width + 1,
                                                            self.button_height + 1), 1)
            pygame.draw.rect(screen, self.frame_color, pygame.Rect(self.left + 2,
                                                                   (c - 1) * self.middle + (
                                                                               c - 1) * self.button_height + 50 + 2,
                                                                   self.button_width - 2,
                                                                   self.button_height - 2), 1)
            a = self.font.render(i, 1, (10, 10, 10))
            text_rect = a.get_rect(center=(800 / 2, c * (self.middle + self.button_height) + 10))
            screen.blit(a, text_rect)

    def render_records_menu(self, list_of_records):
        screen = self.screen
        screen.fill((100, 100, 100))
        heading = "RECORDS: 9 x 9"
        if list_of_records == self.In_5: heading = "RECORDS: 5 x 5"
        a = self.font.render(heading, 1, (255, 255, 255))
        text_rect = a.get_rect(center=(800 / 2, 50))
        screen.blit(a, text_rect)
        c = 1
        ind = -1
        self.middle = 5
        self.button_height = 25
        self.button_width = 300
        self.left = 250
        for i in list_of_records[:11]:
            ind += 1
            c += 1
            pygame.draw.polygon(screen, self.button_color, [
                (self.left, (c - 1) * self.middle + (c - 1) * self.button_height + 80),
                (self.left, (c - 1) * self.middle + c * self.button_height + 80),
                (self.left + self.button_width, (c - 1) * self.middle + c * self.button_height + 80),
                (self.left + self.button_width, (c - 1) * self.middle + (c - 1) * self.button_height + 80)])
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.left,
                                                            (c - 1) * self.middle + (c - 1) * self.button_height + 80,
                                                            self.button_width + 1,
                                                            self.button_height + 1), 1)
            pygame.draw.rect(screen, self.frame_color, pygame.Rect(self.left + 2,
                                                                   (c - 1) * self.middle + (
                                                                           c - 1) * self.button_height + 80 + 2,
                                                                   self.button_width - 2,
                                                                   self.button_height - 2), 1)
            i = f"{ind}. | {i[2]} | {i[0]}"
            a = self.font.render(i, 1, (10, 10, 10))
            text_rect = a.get_rect(center=(800 / 2, c * (self.middle + self.button_height) + 64))
            screen.blit(a, text_rect)
        self.middle = 20
        self.button_width = 150
        self.button_height = 40
        self.left = 325
        c = 8
        pygame.draw.polygon(screen, self.button_color, [
            (self.left, (c - 1) * self.middle + (c - 1) * self.button_height + 50),
            (self.left, (c - 1) * self.middle + c * self.button_height + 50),
            (self.left + self.button_width, (c - 1) * self.middle + c * self.button_height + 50),
            (self.left + self.button_width, (c - 1) * self.middle + (c - 1) * self.button_height + 50)])
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.left,
                                                        (c - 1) * self.middle + (c - 1) * self.button_height + 50,
                                                        self.button_width + 1,
                                                        self.button_height + 1), 1)
        pygame.draw.rect(screen, self.frame_color, pygame.Rect(self.left + 2,
                                                               (c - 1) * self.middle + (
                                                                       c - 1) * self.button_height + 50 + 2,
                                                               self.button_width - 2,
                                                               self.button_height - 2), 1)
        a = self.font.render("Back", 1, (10, 10, 10))
        text_rect = a.get_rect(center=(800 / 2, c * (self.middle + self.button_height) + 10))
        screen.blit(a, text_rect)


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
        menu = Menu(screen, Font, "Start")
        menu.render_menu(screen)
        menu_flag = True
        running = True
        menu_flag_2 = True
        while menu_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    run = False
                    menu_flag = False
                    menu_flag_2 = False
                if event.type == pygame.MOUSEBUTTONDOWN and menu.action_allowed:
                    menu.get_click(event.pos)
            pygame.display.flip()

        board = Board(menu.Board_size, menu.Board_size, screen, Font)
        board.render(screen, Font)
        board.gamemove(screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    run = False
                    menu_flag = False
                    menu_flag_2 = False
                if event.type == pygame.MOUSEBUTTONDOWN and board.action_allowed:
                    board.get_click(event.pos)
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        running = False
                        menu_flag_2 = False
                        break
            pygame.display.flip()

        menu = Menu(screen, Font, "End")
        menu.render_menu(screen)
        while menu_flag_2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    run = False
                    menu_flag = False
                    menu_flag_2 = False
                if event.type == pygame.MOUSEBUTTONDOWN and menu.action_allowed:
                    menu.get_click(event.pos)
            pygame.display.flip()

    # завершение работы
    pygame.quit()