from tkinter import Button, Frame
from cell import Cell



class Cheat_Button:
    """Читерская кнопка показывает где мины"""

    def __init__(self) -> None:
        self.button_object = None
        self.is_clicked = False

    def create_button_object(self, location: Frame) -> None:
        """Создает объект кнопки и биндит клавиши к ней"""

        button = Button(
                location,
                width=12,
                height=4,
                bg='Black'
                )

        button.bind('<Button-1>', self.left_click_actions)

        self.button_object = button

    def left_click_actions(self, _) -> None:
        """Логика кнопки при нажатии ЛКМ"""
        
        if not self.is_clicked:
            self.is_clicked = True
            self.show_or_hide_all_mines()
        else:
            self.is_clicked = False
            self.show_or_hide_all_mines()

    def show_or_hide_all_mines(self) -> None:
        """Показывает или скрывает все мины"""
        
        mine_list = [cell for cell in Cell.all_cells_list if cell.is_mine]

        if self.is_clicked:
            for mine in mine_list:
                mine.cell_button_object.configure(
                    bg='#434570'
                )
        else:
            for mine in mine_list:
                if mine.is_mine_suspected:
                    mine.cell_button_object.configure(
                        bg='#535757'
                    )
                else:
                    mine.cell_button_object.configure(
                        bg='SystemButtonFace'
                    )


