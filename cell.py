from tkinter import Button, Label
import random
import settings
import ctypes
import sys



class Cell:
    """Класс клетки на поле"""

    all_cells_list = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    def __init__(self, x: int, y: int, is_mine: bool=False) -> None:
        self.is_opened = False
        self.is_mine_suspected = False
        self.cell_button_object = None
        self.is_mine = is_mine
        self.x = x
        self.y = y
        
        # Append the object to Cell.all_cells_list
        Cell.all_cells_list.append(self)

    def __repr__(self) -> str:
        return f'Cell({self.x}, {self.y})'

    def create_button_object(self, location) -> None:
        """Создает объект кнопки и биндит клавиши миши к ней"""
        
        button = Button(
            location,
            width=12,
            height=4,
        )

        button.bind('<Button-1>', self.left_click_actions) # Left click
        button.bind('<Button-3>', self.right_click_actions) # Right click
        
        self.cell_button_object = button

    def left_click_actions(self, _) -> None:
        """Логика клетки при нажатии ЛКМ"""
        
        if self.is_mine:
            self.show_mine()
        else:
            if not self.surrounded_cells_mines_amount:
                for cell_object in self.surrounded_cells_list: 
                    cell_object.show_cell()
                    cell_object.cell_button_object.configure(
                        bg=cell_object.get_color()
                    )

            self.show_cell()
            self.cell_button_object.configure(
                        bg=self.get_color()
            )

            # If Mines count is equal to the cells left count, player won
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'Game Over', 0)

        # Cancel Left and Right click events if cell is already opened:
        self.cell_button_object.unbind('<Button-1>')
        self.cell_button_object.unbind('<Button-3>')   

    def right_click_actions(self, _) -> None:
        """Логика клетки при нажатии ПКМ"""
        
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
        """Cписок окружающих клеток"""
        
        surrounded_cells = []
        
        # Fill the surrounded_cells list with surrounded cells
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if self.x == i and self.y == j:
                    continue
                
                surrounded_cells.append(self.get_cell_by_axis(i, j))
        
        surrounded_cells = [cell for cell in surrounded_cells if cell is not None]
        
        return surrounded_cells

    @property
    def surrounded_cells_mines_amount(self) -> int:
        """Счетчик количества мин вокруг клетки"""
        
        counter = 0
        
        for cell in self.surrounded_cells_list:
            if cell.is_mine:
                counter += 1
        
        return counter

    def show_cell(self) -> None:
        """Открывает клетку"""

        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_button_object.configure(
                text=self.surrounded_cells_mines_amount \
                if self.surrounded_cells_mines_amount else ''
            )
            
            # Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f'Cells left: {Cell.cell_count}'
                )

            # If this was a mine suspect, then for safety, we should
            # configure the background to SystemButtonFace
            self.cell_button_object.configure(
                bg='SystemButtonFace'
            )
        
        # Mark the cell as opened
        self.is_opened = True

    def show_mine(self) -> None:
        """Открывает мину и завершает игру"""

        ctypes.windll.user32.MessageBoxW(0, 'You have been blown up', 'Game Over', 0)
        sys.exit()

    def get_color(self) -> str:
        """
        В зависимости от кол-ва мин вокруг клетки
        задает определенный цвет
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

        return colors_dict.get(self.surrounded_cells_mines_amount)
    
    @staticmethod
    def create_cell_count_label(location) -> None:
        """Создает текст счетчика оставшихся клеток"""
        
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
        """Возвращает объект клетки основываясь на значениях x и y"""
        
        for cell in Cell.all_cells_list:
            if cell.x == x and cell.y == y:
                return cell

    @staticmethod
    def randomize_mines() -> None:
        """Случайно выбирает мины из клеток"""
        
        picked_cells = random.sample(
            Cell.all_cells_list,
            settings.MINES_COUNT
        )
        
        for cell in picked_cells:
            cell.is_mine = True