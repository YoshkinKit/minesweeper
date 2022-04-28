from tkinter import *
from tkinter.font import Font
import settings
import utils
from cell import Cell
from cheat_button import Cheat_Button



root = Tk()

# Override the settings of the window
root.configure(bg='black')
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title('Minesweeper Game')
root.resizable(False, False)

font = Font(
    family='Comic Sans MS', 
    size=30, 
    weight='bold', 
    slant='italic'
)

top_frame = Frame(
    root,
    bg='black', 
    width=settings.WIDTH,
    height=utils.get_height_by_percentage(25),
)
top_frame.place(
    x=0,
    y=0,
)

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text='Minesweeper Game',
    font=font,
)
game_title.place(
    x=utils.get_width_by_percentage(32),
    y=utils.get_height_by_percentage(8),
)

cheat_button = Cheat_Button()
cheat_button.create_button_object(top_frame)
cheat_button.button_object.place(
    x=0,
    y=0,
)

left_frame = Frame(
    root,
    bg='black',
    width=utils.get_width_by_percentage(25),
    height=utils.get_height_by_percentage(75),
)
left_frame.place(
    x=0, 
    y=utils.get_height_by_percentage(25),
)

center_frame = Frame(
    root,
    bg='black', 
    width=utils.get_width_by_percentage(75),
    height=utils.get_height_by_percentage(75),
)
center_frame.place(
    x=utils.get_width_by_percentage(25),
    y=utils.get_height_by_percentage(25),
)

# Creating field of size GRID_SIZExGRID_SIZE
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        cell = Cell(x, y)
        cell.create_button_object(center_frame)
        cell.cell_button_object.grid(
            column=y,
            row=x
        )

# Call the label from the Cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(
    x=utils.get_width_by_percentage(2),
    y=utils.get_height_by_percentage(15),
)
Cell.cell_count_label_object.configure(font=font)

Cell.randomize_mines()

# Run the window
root.mainloop()