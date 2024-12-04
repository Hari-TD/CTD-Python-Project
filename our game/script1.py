import tkinter as tk
from tkinter import messagebox
import random

window = tk.Tk()
window.title("Maze Navigator")

grid_size = 20  # 20x20 grid
cell_size = 25  # 25px per grid cell
player_position = [11, 6]

Locations = {
    "Tang Zheng Tang, Chinese Pavilion": (10, 1),
    "Gym": (16, 8),
    "T-lab": (6, 15),
    "OneStop Centre": (9, 15),
    "Albert Hong Lecture Theatre": (5, 17),
    "Scrapyard": (8, 8),
    "Swimming pool": (17, 5),
    "Fab-Lab": (6, 9),
    "Upper Changi MRT": (2, 15),
    "D'Star Bistro": (7, 15),
    "Campus Centre": (8, 15),
    "Vending machines": (5, 13)
}

final_destination = None
final_destination_name = None

walls = [(0, 13), (0, 14), (1, 10), (1, 11), (1, 12),(1,13),(1,14),(2,10),(2,11),(2,12),(2,13),(2,14),(2,16),(2,17),(3,12),(3,13),(3,14),(3,16),(3,17),(3,18),(4,12),(4,13),(4,14),(4,16),(4,17),(4,18),(5,6),(5,7),(5,8),(5,9),(6,12),(6,13),(6,14),(6,16),(6,17),(6,18),(7,9),(7,11),(7,12),(7,13),(7,14),(7,16),(7,17),(7,18),(8,7),(8,9),(9,3),(10,1),(10,4),(10,8),(10,12),(10,13),(10,14),(11,11),(11,14),(12,6),(13,0),(13,3),(13,7),(14,1),(14,4),(15,2),(15,5),(15,9),(16,3),(16,9),(16,10),(17,7),(18,8),(18,10),(18,11),(18,12),(19,5),(19,6),(19,10),(19,11)]

canvas = tk.Canvas(window, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

player = None

def choose_final_destination():
    global final_destination, final_destination_name
    final_destination_name = random.choice(list(Locations.keys()))
    final_destination = Locations[final_destination_name]
    return final_destination_name

def show_instructions():
    messagebox.showinfo(
        "Instructions\n"
        "Welcome to Maze Navigator!\n\n"
        "Use the W, A, S, D keys to move:\n"
        "W = Up, S = Down, A = Left, D = Right.\n\n"
        "A description will be given to you, and your goal is to travel to the described location in SUTD."
        "note: do not walk into the walls! (marked by solid lines)"
    )

def show_clue(destination_name):
    clue = Locations[destination_name]
    messagebox.showinfo("Clue", f"Clue: {clue}")

def move_player(postal_code):
    global player_position
    moves = {"1": (-1, 0), "2": (1, 0), "3": (0, -1), "4": (0, 1)}
    if postal_code in moves:
        dx, dy = moves[postal_code]
        new_x = player_position[0] + dx
        new_y = player_position[1] + dy
        if (0 <= new_x < grid_size and 0 <= new_y < grid_size) and (new_x, new_y) not in walls:
            player_position = [new_x, new_y]
            update_player_position()
        else:
            messagebox.showinfo("Blocked", "You hit a wall! Try a different direction.")

def update_player_position():
    canvas.coords(player, player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
                  player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10)
    check_win_condition()

def check_win_condition():
    if tuple(player_position) == final_destination:
        messagebox.showinfo("Congratulations!", f"You reached {final_destination_name}!")
        canvas.create_text(
            grid_size * cell_size // 2,
            grid_size * cell_size // 2,
            text="You Win!",
            font=("Arial", 24),
            fill="green"
        )

def direction_to_destination():
    player_x, player_y = player_position
    dest_x, dest_y = final_destination
    
    direction = ""
    if player_x < dest_x:
        direction = "Move Down"
    elif player_x > dest_x:
        direction = "Move Up"
    
    if player_y < dest_y:
        direction += " and Move Right"
    elif player_y > dest_y:
        direction += " and Move Left"
    
    if direction:
        messagebox.showinfo("Direction", f"Direction to {final_destination_name}: {direction}")

def handle_keypress(event):
    key_to_postal = {"w": "1", "s": "2", "a": "3", "d": "4"}
    if event.char in key_to_postal:
        move_player(key_to_postal[event.char])

def start_game():
    choose_final_destination()
    draw_grid()
    draw_start_end()
    show_instructions()
    show_clue(final_destination_name)

def restart_game():
    global player_position, player
    player_position = [11,6]
    canvas.delete("all")  # Clear the canvas
    choose_final_destination()  # Reinitialize final destination
    draw_grid()  # Redraw the grid
    draw_start_end()  # Redraw the start and final destination
    player = canvas.create_oval(
        player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
        player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10,
        fill="blue"
    )

def exit_game():
    window.quit()

def draw_grid():
    for i in range(grid_size):
        for j in range(grid_size):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if (i, j) in walls:
                canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")  # Wall
            else:
                canvas.create_rectangle(x1, y1, x2, y2, outline="black")  # Regular cell

def draw_start_end():
    canvas.create_rectangle(player_position[0] * cell_size, player_position[1] * cell_size,
                            player_position[0] * cell_size + cell_size, player_position[1] * cell_size + cell_size,
                            fill="green")
    canvas.create_rectangle(final_destination[0] * cell_size, final_destination[1] * cell_size,
                            final_destination[0] * cell_size + cell_size, final_destination[1] * cell_size + cell_size,
                            fill="red")

restart_button = tk.Button(window, text="Restart", command=restart_game)
restart_button.pack(side="left", padx=20)

exit_button = tk.Button(window, text="Exit", command=exit_game)
exit_button.pack(side="left", padx=20)

choose_final_destination()
draw_grid()
draw_start_end()
player = canvas.create_oval(
    player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
    player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10,
    fill="blue"
)
start_game()

window.bind("<Key>", handle_keypress)

window.mainloop()
