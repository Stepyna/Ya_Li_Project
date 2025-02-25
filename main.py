import pygame
import random
import copy
import csv
import pygame_menu

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

def menu_manage():
    pass

def false_flags():
    global menu_flag
    global running
    global menu_flag_2
    global esc_flag
    global record_flag
    global run_main_menu
    global first_time
    global options_flag
    global rules_flag
    menu_flag = False
    running = False
    menu_flag_2 = False
    esc_flag = False
    record_flag = False
    run_main_menu = True
    first_time = False
    options_flag = False
    rules_flag = False
    with open('options.csv', encoding="utf8", mode="w") as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"')
        writer.writerow(["VOLUME"])
        writer.writerow([VOLUME])
        csvfile.close()
    exit()


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

    def update_upper(self):
        pygame.draw.polygon(self.screen, (200, 200, 200), [(0, 0), (0, 54), (800, 54), (800, 0)])
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 55), self.frame_size)
        a = self.Font.render(f'Score: {self.score}', 1, (255, 255, 255))
        screen.blit(a, (500, 20))
        a = Font.render("Next:", 1, (255, 255, 255))
        screen.blit(a, (250, 20))
        for i in [3, 4, 5]:
            pygame.draw.polygon(screen, self.cell_color, [
                (175 + i * self.cell_size, 2),
                (175 + i * self.cell_size, self.cell_size),
                (175 + (i + 1) * self.cell_size, self.cell_size),
                (175 + (i + 1) * self.cell_size, 2)])

            pygame.draw.rect(screen, self.frame_color,
                             pygame.Rect(175 + i * self.cell_size + 2,
                                         2,
                                         self.cell_size - 3,
                                         self.cell_size - 3), self.frame_size)

            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(175 + i * self.cell_size,
                                                            2,
                                                            self.cell_size + 1,
                                                            self.cell_size + 1), self.frame_size)

            for i in [4, 5, 6]:
                pygame.draw.circle(screen, self.color_dict[self.generated_balls[i - 4]],
                                   (175 + i * self.cell_size - self.cell_size // 2,
                                    self.cell_size // 2 + 2), self.ball_radius, 20)

                pygame.draw.circle(screen, (0, 0, 0),
                                   (175 + i * self.cell_size - self.cell_size // 2,
                                    self.cell_size // 2 + 2), self.ball_radius,
                                   2)

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
        self.update_second_board()
        self.update_upper()

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
        self.update_upper()

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
        if 1 <= self.prev_column <= self.width and 1 <= self.prev_row <= self.height: self.fill_cell(self.prev_row,
                                                                                                     self.prev_column,
                                                                                                     self.cell_color)
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
        im = pygame.image.load("data/retro_moscow_3.png")
        rect = im.get_rect(bottomright=(800, 600))
        screen.blit(im, rect)
        count_column = 0
        count_row = 0
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
             self.left - 1,
             self.top - 1,
             self.width * self.cell_size + 3,
             self.width * self.cell_size + 3), 1)
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
        self.update_second_board()

    def end_of_game(self):
        global running
        global NAME
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
                writer.writerow([NAME, self.width, self.score])
            csvfile.close()
        running = False


class Menu(pygame_menu.Menu):
    def __init__(self, heading, x_coord, y_coord, flag, screen, Font, page, mode):
        super().__init__(heading, x_coord, y_coord, theme=flag)
        self.screen = screen
        self.font = Font
        self.mode = mode
        self.enable()
        self.num_page = page
        self.dict_of_text = ["""COLOR LINES

The essence of the game is to get 
as many points as possible.""",
                             """Points are obtained for collecting as many balls
as possible in one row, column or diagonal by
moving them one at a time. The ball will move 
if it has the opportunity to pass to the selected 
cell from the one in which he is now with non-diagonal
path. For collecting more balls in one line 
at a time, the player is given 
significantly more points than for less.""",
                             """When collecting balls, they collapse, immediately 
adding points to the counter and 
disappearing from the field. 
The course of the game 
begins with the appearance of 
new balls in random cells of the field. 
Colors of the following balls the 
player knows the move in advance.""",

"""Controls

Left mouse button to select ball or cell or 
to use button;
Esc to pause the game;
Left and right arrows to select pages or change 
difficulties in menus when change buttons are selected"""]
        self.LABEL_TEXT = self.dict_of_text[self.num_page - 1]
        if self.mode == "start":
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
                    else:
                        In_9.append(row)
            self.In_5 = sorted(In_5, key=lambda x: x[2])
            self.In_9 = sorted(In_9, key=lambda x: x[2])
            self.difficulty = 9
            self.value = (('9x9', 9), 0)
            self.dict_1 = {9: self.In_9,
                           5: self.In_5
                           }
            csvfile.close()

        self.list_of_buttons = []

    def new_name(self, name):
        global NAME
        NAME = name

    def set_difficulty(self, val, diff):
        global DIFF
        global VAL
        DIFF, VAL = diff, val
        self.difficulty = diff
        self.value =  val

    def start_the_game(self):
        global DIFF
        DIFF = self.difficulty
        self.disable()

    def records(self):
        global record_flag
        global first_time
        global run_main_menu
        record_flag = True
        run_main_menu = False
        first_time = True

    def options(self):
        global options_flag
        global first_time
        global run_main_menu
        options_flag = True
        run_main_menu = False
        first_time = True

    def rules(self):
        global rules_flag
        global first_time
        global run_main_menu
        global flag_change
        rules_flag = True
        run_main_menu = False
        first_time = True
        flag_change = True

    def back(self):
        global run_main_menu
        global rules_flag
        global options_flag
        global record_flag
        global first_time
        first_time = True
        options_flag = False
        rules_flag = False
        record_flag = False
        run_main_menu = True

    def minus_page(self, a, b):
        global flag_change
        global first_time
        self.num_page = b
        if self.num_page == 5: self.num_page = 4
        self.LABEL_TEXT = self.dict_of_text[self.num_page - 1]
        flag_change = True
        first_time = True

    def plus_page(self, a, b):
        global flag_change
        global first_time
        self.num_page = b
        if self.num_page == 5: self.num_page = 1
        self.LABEL_TEXT = self.dict_of_text[self.num_page - 1]
        flag_change = True
        first_time = True

    def resume_the_game(self):
        self.disable()

    def main_menu(self):
        global menu_flag_2
        global running
        global first_time
        menu_flag_2, running = False, False
        first_time = True

    def volume(self, val):
        global VOLUME
        VOLUME = val


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    pygame.display.set_caption("Color Lines")
    pygame.font.init()
    path = pygame.font.match_font("nunito")
    Font = pygame.font.Font(path, 30)
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    run = True
    DIFF = 9
    NAME = "You"
    myimage = pygame_menu.baseimage.BaseImage(
        image_path="data/retro_moscow_3.png",
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY)
    mytheme = pygame_menu.themes.Theme(background_color=myimage,  # transparent background
                    title_background_color=(200, 200, 200),
                    widget_font=pygame_menu.font.FONT_NEVIS,
                    widget_font_background_color=(200, 200, 200),
                    title_font_color=(60, 60, 60),
                    widget_font_color=(60, 60, 60))
    with open('options.csv', encoding="utf8", mode="r") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for i in reader:
            VOLUME = i[0]

    VOLUME = float(VOLUME)

    # основной цикл
    while run:
        menu = Menu('COLOR LINES', 800, 600, mytheme, screen, Font, 1, "start")
        menu.add.text_input('Name :', default='You', onchange=menu.new_name)
        DIFF = menu.difficulty
        VAL = menu.value
        menu.add.selector('Difficulty :', [('9x9', 9), ('5x5', 5)], onchange=menu.set_difficulty)
        menu.add.button('Play', menu.start_the_game)
        menu.add.button('Records', menu.records)
        menu.add.button('Options', menu.options)
        menu.add.button('Rules', menu.rules)
        menu.add.button('Quit', false_flags)
        menu_flag = True
        running = True
        menu_flag_2 = True
        esc_flag = False
        record_flag = False
        run_main_menu = True
        first_time = True
        options_flag = False
        rules_flag = False
        flag_change = True
        # Цикл начального меню
        while menu_flag:
            menu_manage()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    false_flags()
            if menu.is_enabled():
                menu.draw(screen)
                menu.update(events)

            else: break

            if run_main_menu:
                if not (record_flag or options_flag or rules_flag) and first_time:
                    first_time = False
                    menu = Menu('COLOR LINES', 800, 600, mytheme, screen, Font, 1, "start")
                    menu.add.text_input('Name :', default=NAME, onchange=menu.new_name, maxchar=15)
                    menu.add.selector('Difficulty :', [('9x9', 9), ('5x5', 5)], default=[9, 5].index(DIFF), onchange=menu.set_difficulty)
                    menu.add.button('Play', menu.start_the_game)
                    menu.add.button('Records', menu.records)
                    menu.add.button('Options', menu.options)
                    menu.add.button('Rules', menu.rules)
                    menu.add.button('Quit', false_flags)

            if record_flag:
                if not run_main_menu and first_time:
                    first_time = False
                    menu = Menu(f'RECORDS {VAL[0][0]}', 800, 600, mytheme, screen, Font, 1, "start")
                    c, ind = 1, -1
                    for i in menu.dict_1[DIFF][:11]:
                        ind += 1
                        c += 1
                        i = f"{ind}. | {i[2]} | {i[0]}"
                        menu.add.label(i)
                    menu.add.button("Back", menu.back)

            if rules_flag:
                if not run_main_menu and first_time:
                    if flag_change:
                        menu = Menu('RULES', 800, 600, mytheme, screen, Font, menu.num_page, "start")
                        menu.add.selector('PAGE :', [('1', 1), ('2', 2), ("3", 3), ("4", 4)], default=menu.num_page - 1, onchange=menu.plus_page, onreturn=menu.minus_page)
                        menu.add.label(menu.LABEL_TEXT)
                        menu.add.button("Back", menu.back)
                        flag_change = False
                        first_time = False

            if options_flag:
                if not run_main_menu and first_time:
                    first_time = False
                    menu = Menu("OPTIONS", 800, 600, mytheme, screen, Font, 1, "start")
                    menu.add.range_slider("Volume:", VOLUME, [0, 100], 1, menu.volume)
                    menu.add.button("Back", menu.back)

            pygame.display.update()

        board = Board(DIFF, DIFF, screen, Font)
        board.render(screen, Font)
        board.gamemove(screen)
        # Цикл поля и меню паузы
        while running:
            for event in pygame.event.get():
                while esc_flag:
                    menu_manage()
                    events = pygame.event.get()
                    for ev in events:
                        if ev.type == pygame.QUIT:
                            false_flags()
                    if menu.is_enabled():
                        menu.draw(screen)
                        menu.update(events)
                    else:
                        esc_flag = False
                        board.render(screen, Font)
                        board.clickedFlag = False
                        board.update_board(screen)
                        board.update_upper()
                    if not running: break
                    pygame.display.update()
                else:
                    pygame.display.flip()
                    if event.type == pygame.QUIT:
                        running = False
                        run = False
                        menu_flag = False
                        menu_flag_2 = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN and board.action_allowed:
                        board.get_click(event.pos)
                    if event.type == pygame.KEYDOWN:
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            esc_flag = True
                            menu = Menu('PAUSE', 800, 600, mytheme, screen, Font, 1,"esc")
                            menu.add.button('Resume', menu.resume_the_game)
                            menu.add.button('Main menu', menu.main_menu)
                            menu.add.button('Quit', false_flags)
                    pygame.display.flip()

        menu = Menu('GAME OVER', 800, 600, mytheme, screen, Font, 1,"end")
        menu.add.label(f'"{NAME}" scored: {board.score}')
        menu.add.button('Main menu', menu.main_menu)
        menu.add.button('Quit', false_flags)
        menu.disable()
        # Цикл финального меню
        while menu_flag_2:
            menu_manage()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    false_flags()
            if menu.is_enabled():
                menu.draw(screen)
                menu.update(events)
            else:
                menu.enable()
            pygame.display.update()

    # завершение работы
    with open('options.csv', encoding="utf8", mode="w") as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"')
        writer.writerow(["VOLUME"])
        writer.writerow([VOLUME])
        csvfile.close()
    pygame.quit()