import json
import time
import os
import random

save_file = 'save.json'
score = 0
click = 1


def save_game(score, click):
    data = {'score': score, 'click': click}
    with open(save_file, 'w') as f:
        json.dump(data, f)

    print("game saved")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


yel = "\033[33m"
blu = "\033[94m"
r = "\033[0m"
red = "\033[31m"
pur = "\033[95m"
gre = "\033[32m"


def login():
    if os.path.exists("system.json"):
        with open("system.json", "r") as f:
            loaded_data = json.load(f)
            print(f"hi, {loaded_data['user']}!")
    else:
        reg()


def login2():
    if os.path.exists('system.json'):
        with open('system.json', 'r') as logn:
            load_user = json.load(logn)

            return f"{gre}╰┌[{red}{load_user['user']}]{gre}─[{blu}/home{gre}]┐╯{r}\n{gre} ╰─|{r}"
    else:
        return f"{gre}╰┌[{red}guest]{gre}─[{blu}/home{gre}]┐╯{r}\n{gre} ╰─|{r}"
 

def bootshop():
    if os.path.exists('system.json'):
        with open('system.json', 'r') as shop:
            user_shop = json.load(shop)

            return f"{gre} ┗━━━━━━━━━━━━━━━┓\n{red}{user_shop['user']}{r} _shop.>> "
    else:
        return f'{red}guest{r} {yel}>>>{r}'


def loading():
    dots = 0
    for i in range(3):
        dots += 1
        print("loading" + " ∘" * dots)
        time.sleep(0.5)
        clear()


def menu():
    print(f"{yel}._____________________________.{r}")
    print(f"{yel}| {blu}OS name: Windows Dos xp     ")
    print(f"{yel}| {blu}RAM need: ∞ GB              ")
    print(f"{yel}| {blu}CPU need: intel core I∞ ∞K  ")
    print(f"{yel}|{blu} GPU need: RTX∞              ")
    print(f"{yel}|_____________________________|{r}")


def game3():
    while True:
        from random import randint

        import pygame
        import sys

        # Размеры поля и сетки:
        SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
        GRID_SIZE = 20
        GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
        GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

        # Направления движения:
        UP = (0, -1)
        DOWN = (0, 1)
        LEFT = (-1, 0)
        RIGHT = (1, 0)

        # Допустимый набор команд управления змейкой с клавиатуры
        POSSIBLE_ACTIONS = {
            (pygame.K_UP, RIGHT): UP,
            (pygame.K_UP, LEFT): UP,
            (pygame.K_DOWN, RIGHT): DOWN,
            (pygame.K_DOWN, LEFT): DOWN,
            (pygame.K_LEFT, UP): LEFT,
            (pygame.K_LEFT, DOWN): LEFT,
            (pygame.K_RIGHT, UP): RIGHT,
            (pygame.K_RIGHT, DOWN): RIGHT
        }

        # Цвет фона - черный:
        BOARD_BACKGROUND_COLOR = (0, 0, 0)

        # Цвет границы ячейки - голубовато-бирюзовый:
        BORDER_COLOR = (93, 216, 228)

        # Цвет яблока - красный:
        APPLE_COLOR = (255, 0, 0)

        # Цвет змейки - зеленый:
        SNAKE_COLOR = (0, 200, 100)

        # Скорость змейки: пауза 1/20 секунды в каждой итерации игового цикла:
        SPEED = 10

        # Системные настройки и инициализация графики.
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption('Змейка')

        clock = pygame.time.Clock()

        class GameExitException(Exception):
            """Исключение, которое выбрасывается для выхода из игры."""

        class GameObject:
            """Описывает базовые свойства, общие для всех игровых объектов.
            Атрибуты:
                position (tuple): Кортеж из двух целых чисел, представляющий координаты
                объекта на экране.
                body_color (tuple): Кортеж из трех целых чисел (R,G,B), представляющий
                цвет для отрисовки объекта.
            """

            def __init__(self):
                """Инициализирует базовый игровой объект.
                Объект размещается в центре экрана, цвет остается неопределенным.
                """
                self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
                self.body_color = None

            def draw(self):
                """Отрисовка игрового объекта.
                Реализуется в дочерних классах конкретных игровых объектов на экране.
                """

            @staticmethod
            def draw_rect(position_of_rect, color_of_rect, is_border=True):
                """Отрисовка одной ячейки на игровом поле.
                Входные параметры: координаты, цвет, признак отрисовки контура.
                """
                rect = pygame.Rect(position_of_rect, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, color_of_rect, rect)
                if is_border:
                    pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        class Apple(GameObject):
            """Описывает игровой объект Яблоко.
            Атрибуты:
                position (tuple): Кортеж из двух целых чисел, представляющий координаты
                объекта на экране.
                body_color (tuple): Кортеж из трех целых чисел (R,G,B), представляющий
                цвет для отрисовки объекта.
            """

            def __init__(self,
                        color_of_apple=APPLE_COLOR,
                        blocked_positions=None
                        ) -> None:
                """Инициализирует игровой объект Яблоко.
                Объект позиционируется в случайном положении на экране, цвет
                по-умолчанию задается зеленый.
                """
                super().__init__()
                self.body_color = color_of_apple
                self.randomize_position(blocked_positions)

            @staticmethod
            def get_random_position_on_screen() -> tuple:
                """Вычисление координат случайной ячейки на поле, возвращает кортеж из
                двух целых чисел, представляющий координаты на экране.
                """
                coord_x_limit = (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE
                coord_y_limit = (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE
                coord_x = randint(0, coord_x_limit)
                coord_y = randint(0, coord_y_limit)
                return (coord_x * GRID_SIZE, coord_y * GRID_SIZE)

            def randomize_position(self, bad_positions: list) -> None:
                """Генерация случайного местоположения яблока на поле с учетом занятых
                другими игровыми объектами ячеек на поле.
                Список занятых на экране ячеек передается в параметре функции.
                """
                new_site = self.get_random_position_on_screen()
                while new_site in (bad_positions if bad_positions is not None else []):
                    new_site = self.get_random_position_on_screen()
                self.position = new_site

            def draw(self):
                """Отображение яблока на игровом поле. Закрашивается квадрат зеленым
                цветом, по контуру рисуется рамка.
                """
                self.draw_rect(self.position, self.body_color)

        class Snake(GameObject):
            """Описывает игровой объект Змейка.
            Атрибуты:
                position [(tuple)]: Список, содержащий кортежи из двух целых чисел,
                представляющие координаты каждого элемента тела змейки.
                last (tuple): Кортеж, содержащий координаты хвоста змеи.
                direction (tuple): Кортеж их двух целых чисел в диапазоне [-1..1],
                описывающих направление движение по оси Х и У за каждый ход.
                body_color (tuple): Кортеж из трех целых чисел (R,G,B), представляющий
                цвет для отрисовки объекта.
                add_length (bool): Признак удлинения змейки при съедании яблока.
            """

            def __init__(self, color_of_snake=SNAKE_COLOR):
                """Инициализирует игровой объект Змейка.
                При создании объекта его позиция устанавливается в центре экрана, цвет
                задается зеленый, определяются координаты хвоста, задается начальное
                направление движения направо.
                """
                super().__init__()
                self.body_color = color_of_snake
                self._initialize_snake()

            def _initialize_snake(self):
                """Инициализирует или сбрасывает состояние змейки."""
                self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
                self.last = self.positions[0]
                self.direction = RIGHT
                self.next_direction = None
                self.add_length = False

            def get_head_position(self) -> tuple:
                """Получение координат головы змейки."""
                return self.positions[0]

            def get_new_position(self) -> tuple:
                """Вычисление новых координат головы змейки с учетом направления
                движения.
                """
                head_x, head_y = self.get_head_position()
                movement_on_x, movement_on_y = self.direction
                new_coord_x = (head_x + GRID_SIZE * movement_on_x) % SCREEN_WIDTH
                new_coord_y = (head_y + GRID_SIZE * movement_on_y) % SCREEN_HEIGHT
                return new_coord_x, new_coord_y

            def reset(self):
                """Перезапуск игры.
                Имеющаяся змейка закрашивается.
                Новая начальной длины размещается в центре экрана.
                """
                for position in self.positions:
                    self.draw_rect(position, BOARD_BACKGROUND_COLOR, is_border=False)
                if self.last:
                    self.draw_rect(self.last, BOARD_BACKGROUND_COLOR, is_border=False)
                self._initialize_snake()

            def draw(self) -> None:
                """Отображение змейки на игровом поле. Рисуется новая голова, и
                затирается цветом фона хвост змейки.
                """
                if self.last:
                    self.draw_rect(self.last, BOARD_BACKGROUND_COLOR, is_border=False)
                head_position = self.get_head_position()
                self.draw_rect(head_position, self.body_color)

            def update_direction(self, next_direction) -> None:
                """Смена направления движения на следующем ходе."""
                self.direction = next_direction

            def move(self) -> None:
                """Движение змейки. Вычисляются новые координаты головы змеи с учетом
                направления движения и помещаются в начало списка координат змеи.
                Если длину змеи надо увеличить то сохраняем новый хвост из имеющегося.
                Если длина змеи остается прежней, хвост "отбрасывается" для последующей
                затирки.
                """
                new_position = self.get_new_position()
                self.positions.insert(0, new_position)
                if self.add_length:
                    self.last = self.positions[len(self.positions) - 1]
                    self.add_length = False
                else:
                    self.last = self.positions.pop(-1)

            def check_collision(self, occupied_cells=None) -> bool:
                """Проверка столкновения головы змеи с объектами игрового поля.
                По умолчанию проверка только на столкновение со своим телом.
                Опционально можно передать в функцию координаты занятых ячеек в списке
                occupied_cells (например другие игровые объекты, такие, как камни).
                """
                head = self.get_head_position()
                is_occupued_cells = occupied_cells and head in occupied_cells
                return head in self.positions[1:] or is_occupued_cells

        def handle_keys(game_object: Snake):
            """Обработчик нажатия клавиш управления в игре."""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise GameExitException('Игрок вышел из игры.')
                elif event.type == pygame.KEYDOWN:
                    action_variant = (event.key, game_object.direction)
                    if action_variant in POSSIBLE_ACTIONS:
                        game_object.update_direction(POSSIBLE_ACTIONS[action_variant])

        def main():
            """Реализация основного игрового процесса."""
            pygame.init()
            snake = Snake()
            apple = Apple(blocked_positions=snake.positions)
            while True:
                try:
                    handle_keys(snake)
                except GameExitException:
                    pygame.quit()
                    sys.exit('Игрок вышел из игры.')
                snake.move()
                if snake.get_head_position() == apple.position:
                    apple.randomize_position(snake.positions)
                    snake.add_length = True
                if snake.check_collision():
                    snake.reset()
                snake.draw()
                apple.draw()
                pygame.display.update()
                clock.tick(SPEED)

        if __name__ == '__main__':
            main()


def game():
    while True:
        items = ["rock", "paper", "scissors"]
        player_item = input("rock, paper or scissors [exit][1/2/3] ")
        random_item = random.choice(items)
        if random_item == "rock" and player_item == "3":
            print("AI thinking")
            time.sleep(1.5)
            clear()
            print(random_item)
            print("AI won!")
        elif random_item == "rock" and player_item == "2":
            print("AI thinking")
            time.sleep(1.5)
            clear()
            print(random_item)
            print("Player won!")
        elif random_item == "paper" and player_item == "1":
            print("AI thinking")
            time.sleep(1.5)
            clear()
            print(random_item)
            print("AI won!")
        elif random_item == "paper" and player_item == "3":
            print("AI thinking")
            time.sleep(1.5)
            clear()
            print(random_item)
            print("Player won!")
        elif random_item == "scissors" and player_item == "1":
            print("AI thinking")
            time.sleep(1.5)
            clear()
            print(random_item)
            print("Player won!")
        elif random_item == "scissors" and player_item == "2":
            print("AI thinking")
            time.sleep(1.5)
            clear()
            print(random_item)
            print("AI won!")
        elif random_item == "rock" and player_item == "1":
            print("AI thinking")
            time.sleep(1.5)
            clear()
            print(random_item)
            print("Tie")
        elif random_item == "paper" and player_item == "2":
            print("AI thinking")
            time.sleep(1.5)
            clear()
            print(random_item)
            print("Tie")
        elif random_item == 'scissors' and player_item == '3':
            print("AI thinking")
            time.sleep(1.5)
            clear()
            print(random_item)
            print("Tie") 
        if player_item == "exit":
            clear()
            break


def game2():
    numbers = random.randint(1, 10)
    numbers2 = int(input('write number from 1 to 10: '))
    print("AI thinking")
    time.sleep(1.5)
    if numbers == numbers2:
        print("Player won!")
        print(f"AI choose: {numbers}")
    else:
        print('AI won!')
        print(f"AI choose: {numbers}")


print(f"{blu}(Windows Dos xp){r}")
system_data = {}





def reg():
    system_data["user"] = input("User: ")
    system_data["password"] = input("Password: ")


def start_menu():

    print(f"{blu}──────────────────────────────┐{r}")
    print(f"1. {yel}static{r}                    {blu} |{r}")
    print(f"2. {yel}game{r}                      {blu} |{r}")
    print(f"3. {yel}help{r}                       {blu}|{r}")
    print(f"4. {yel}exit{r}                      {blu} |{r}")
    print(f"5. {yel}save to json{r}              {blu} |{r}")
    print(f"6. {yel}load from json{r}            {blu} |{r}")
    print(f"7. {yel}clear{r}                      {blu}|{r}")
    print(f"8. {yel}game2{r}                      {blu}|{r}")
    print(f"9. {pur}game3{r} [{red}beta{r}]        {blu}       |{r}")
    print(f"10. {yel}clicker{r}                  {blu} |{r}")
    print(f"11. {yel}shop{r}                     {blu} |{r}")
    print(f"{blu}┌─────────────────┬───────────┘{r}")


while True:

    registrate = input("login or reg [1/2]: ")
    if registrate == "1" or registrate == "login":
        login()
        break
    elif registrate == "2" or registrate == "reg":
        reg()
        break
    else:
        clear()
        print('choose 1 or 2!')


def loading2():
    dots2 = 0
    for i in range(3):
        dots2 += 1
        print("reboot" + " *" * dots2)
        time.sleep(0.5)
        clear()


def load_game():
    if not os.path.exists(save_file):
        print("no save game")
        return None
    with open(save_file, 'r') as f:
        return json.load(f)


def clicker():
    global click, score
    while True:
        print('1 - click\n2 - stats\n3 - exit\n4 - save game\n5 - load game')
        cmd = input('+>> ')
        if cmd == '1':
            clear()
            score += click
            print(f'+{click} | score = {score}')
        elif cmd == '2':
            clear()
            print(f'score: {score}\nclick: {click}')
        elif cmd == '3':
            clear()
            print('***')
            break
        elif cmd == '4':
            clear()
            save_game(score, click)
        elif cmd == '5':
            clear()
            loaded = load_game()
            if loaded:
                score = loaded['score']
                click = loaded['click']
                print('game loaded')

        else:
            clear()
            print(f'{red}Unknow command{r}')


def upgrade():
    global click, score
    print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    print('┃1. level 1 (+ 1 click power)| cost 100┃')
    print('┃2. level 2 (+ 2 click power)| cost 200┃')
    print('┃3. level 3 (+ 3 click power)| cost 300┃')
    print('┃4. level 4 (+ 4 click power)| cost 400┃')
    print('┃5. level 5 (+ 5 click power)| cost 500┃')
    print('┃6. level 6 (+ 6 click power)| cost 600┃')
    print('┗┓━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
    comm = input(bootshop())
    
    try:
        choice = int(input())
    except ValueError:
        print("write number!")
        return
    if choice == 1 and score >= 100:
        click += 1
        score -= 100
    elif score < 100:
        print("you're poor for this!")
    else:
        print()


while True:
    start_menu()

    com = input(login2())

    clear()

    helper = "all commands: exit, help, static"
    helper2 = "save to json, load fron json, game"
    if com == "4":
        loading2()
        break
    elif com == "3":
        loading()
        print(helper)
        print(helper2)
    elif com == "1":
        loading()
        menu()
    elif com == "2":
        loading()
        game()

    elif com == "5":
        with open("system.json", "w") as f:
            json.dump(system_data, f)

    elif com == "6":
        login()
    elif com == "7":
        clear()
    elif com == "8":
        game2()
    elif com == '9':
        game3()
    elif com == '10':
        clicker()
    elif com == '11':
        upgrade()
    else:
        red = '\033[31m'
        print(f"{red}command not found{r}")
