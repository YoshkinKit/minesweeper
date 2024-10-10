# cell.py
from tkinter import Button, Label, Frame
import random
import settings
import ctypes
import sys


class Cell:
    """Клас клітинки на полі"""

    all_cells_list = []
    cell_count = settings.CELL_COUNT  # Початковий лічильник
    cell_count_label_object = None
    mines_initialized = False  # Відстежує, чи були розміщені міни

    def __init__(self, x: int, y: int, is_mine: bool = False) -> None:
        self.is_opened = False
        self.is_mine_suspected = False
        self.cell_button_object = None
        self.is_mine = is_mine
        self.x = x
        self.y = y

        # Додаємо об'єкт до списку всіх клітинок
        Cell.all_cells_list.append(self)

    def __repr__(self) -> str:
        return f'Cell({self.x}, {self.y})'

    def create_button_object(self, location: Frame) -> None:
        """Створює об'єкт кнопки та прив'язує до неї події миші"""

        button = Button(
            location,
            width=12,
            height=5,
        )

        button.bind('<Button-1>', self.left_click_actions)  # Лівий клік
        button.bind('<Button-3>', self.right_click_actions)  # Правий клік

        self.cell_button_object = button

    def left_click_actions(self, event) -> None:
        """Логіка клітинки при натисканні лівої кнопки миші"""

        if not Cell.mines_initialized:
            # Ініціалізуємо міни після першого кліку
            Cell.initialize_mines(self.x, self.y)
            Cell.mines_initialized = True
            # Встановлюємо правильний лічильник клітинок
            Cell.cell_count = settings.CELL_COUNT - settings.MINES_COUNT

        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_amount == 0:
                for cell_object in self.surrounded_cells_list:
                    if not cell_object.is_opened:
                        cell_object.show_cell()
                        cell_object.cell_button_object.configure(
                            bg=cell_object.get_color()
                        )

            self.show_cell()
            self.cell_button_object.configure(
                bg=self.get_color()
            )

            # Якщо кількість залишених клітинок дорівнює нулю, гравець виграв
            if Cell.cell_count == 0:
                ctypes.windll.user32.MessageBoxW(
                    0,
                    'Вітаємо! Ви виграли гру!',
                    'Перемога',
                    0
                )
                sys.exit()

        # Відв'язуємо події кліків після відкриття клітинки
        self.cell_button_object.unbind('<Button-1>')
        self.cell_button_object.unbind('<Button-3>')

    def right_click_actions(self, event) -> None:
        """Логіка клітинки при натисканні правої кнопки миші"""

        if not self.is_mine_suspected:
            self.cell_button_object.configure(
                bg='#535757'
            )
            self.is_mine_suspected = True
        else:
            self.cell_button_object.configure(
                bg='SystemButtonFace'
            )
            self.is_mine_suspected = False

    @property
    def surrounded_cells_list(self) -> list:
        """Список сусідніх клітинок"""

        surrounded_cells = []

        # Заповнюємо список сусідніх клітинок
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if self.x == i and self.y == j:
                    continue
                cell = self.get_cell_by_axis(i, j)
                if cell:
                    surrounded_cells.append(cell)

        return surrounded_cells

    @property
    def surrounded_cells_mines_amount(self) -> int:
        """Кількість мін навколо клітинки"""

        counter = 0

        for cell in self.surrounded_cells_list:
            if cell.is_mine:
                counter += 1

        return counter

    def show_cell(self) -> None:
        """Відкриває клітинку"""
        if not self.is_opened:
            self.is_opened = True
            Cell.cell_count -= 1
            self.cell_button_object.configure(
                text=str(
                    self.surrounded_cells_mines_amount) if self.surrounded_cells_mines_amount else ''
            )

            # Оновлюємо текст лейбла з кількістю залишених клітинок
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f'Cells left: {Cell.cell_count}'
                )

            # Якщо клітинка була позначена як підозріла на міну, змінюємо фон на стандартний
            self.cell_button_object.configure(
                bg='SystemButtonFace'
            )

    def show_mine(self) -> None:
        """Відкриває міну та завершує гру"""
        ctypes.windll.user32.MessageBoxW(
            0,
            'You have been blown up',
            'Game Over',
            0
        )
        sys.exit()

    def get_color(self) -> str:
        """
        Залежно від кількості мін навколо клітинки задає певний колір
        """

        colors_dict = {
            0: '#A1A6A6',
            1: '#36F585',
            2: '#DEF018',
            3: '#F08418',
            4: '#F01C18',
            5: '#F018AC',
            6: '#DA18F0',
            7: '#181CF0',
            8: '#28F0F7',
        }

        return colors_dict.get(self.surrounded_cells_mines_amount, 'SystemButtonFace')

    @staticmethod
    def create_cell_count_label(location) -> None:
        """Створює текст лейбла з кількістю залишених клітинок"""

        label = Label(
            location,
            bg='black',
            fg='white',
            text=f'Cells left: {Cell.cell_count}',
            width=12,
            height=4,
            font=('', 30),
        )

        Cell.cell_count_label_object = label

    @staticmethod
    def get_cell_by_axis(x: int, y: int):
        """Повертає об'єкт клітинки за координатами x та y"""

        for cell in Cell.all_cells_list:
            if cell.x == x and cell.y == y:
                return cell
        return None

    @staticmethod
    def initialize_mines(first_x: int, first_y: int) -> None:
        """Розміщує міни, виключаючи першу клітинку та її сусідів"""

        # Отримуємо список клітинок, які не повинні містити міни
        safe_cells = Cell.get_adjacent_cells(first_x, first_y)
        first_cell = Cell.get_cell_by_axis(first_x, first_y)
        if first_cell:
            safe_cells.append(first_cell)
        safe_cells = [cell for cell in safe_cells if cell is not None]

        # Вибираємо клітинки для мін, виключаючи безпечні клітинки
        available_cells = [
            cell for cell in Cell.all_cells_list if cell not in safe_cells]

        # Переконуємося, що кількість доступних клітинок достатня для розміщення мін
        if settings.MINES_COUNT > len(available_cells):
            ctypes.windll.user32.MessageBoxW(
                0,
                'Недостатньо клітинок для розміщення всіх мін.',
                'Помилка',
                0
            )
            sys.exit()

        picked_cells = random.sample(
            available_cells,
            settings.MINES_COUNT
        )

        for cell in picked_cells:
            cell.is_mine = True

    @staticmethod
    def get_adjacent_cells(x: int, y: int) -> list:
        """Повертає список клітинок, сусідніх з (x, y)"""

        adjacent_cells = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue
                cell = Cell.get_cell_by_axis(i, j)
                if cell:
                    adjacent_cells.append(cell)
        return adjacent_cells

    @staticmethod
    def randomize_mines() -> None:
        """Метод більше не використовується після впровадження First Click Safety"""
        pass  # Цей метод можна видалити або залишити порожнім
