import tkinter as tk
from tkinter import messagebox
import random
import winsound
from datetime import datetime
root = tk.Tk()
root.title("Neon Tic Tac Toe")
root.state("zoomed")


BG = "#000000"
PANEL_BG = "#111111"
BTN_BG = "#1f1f1f"
NEON_X = "#ffffff"
NEON_O = "#ff2ec8"
TEXT = "#ffffff"
MUTED = "#777777"

root.configure(bg=BG)


sound_on = True
history = []


def turn_sound():
    if sound_on:
        winsound.Beep(650, 120)

def win_sound():
    if sound_on:
        winsound.Beep(1000, 300)

p1_name = ""
p2_name = ""
current = "X"
board = [""] * 9
buttons = []

score_x = 0
score_o = 0
score_draw = 0

game_mode = ""

def clear():
    for w in root.winfo_children():
        w.destroy()

def check_winner(b):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b1,c in wins:
        if b[a] == b[b1] == b[c] != "":
            return b[a]
    if "" not in b:
        return "Draw"
    return None

def ai_move():
    empty = [i for i in range(9) if board[i] == ""]
    if empty:
        click(random.choice(empty))

def click(i):
    global current, score_x, score_o, score_draw

    if board[i] == "":
        board[i] = current
        buttons[i].config(
            text="❌" if current=="X" else "⭕",
            fg=NEON_X if current=="X" else NEON_O
        )

        res = check_winner(board)
        if res:
            win_sound()
            time = datetime.now().strftime("%d-%m-%Y %H:%M")

            if res == "Draw":
                score_draw += 1
                history.append(f"{time} → DRAW")
                result_label.config(text="🤝 MATCH DRAW!", fg="orange")
            elif res == "X":
                score_x += 1
                history.append(f"{time} → {p1_name} WON")
                result_label.config(text=f"🎉 {p1_name} WINS!", fg=NEON_X)
            else:
                score_o += 1
                history.append(f"{time} → {p2_name} WON")
                result_label.config(text=f"🎉 {p2_name} WINS!", fg=NEON_O)

            root.after(1500, reset_board)
        else:
            current = "O" if current == "X" else "X"
            turn_sound()
            update_turn()
            if game_mode == "AI" and current == "O":
                root.after(500, ai_move)
def reset_board():
    global board, current
    board = [""] * 9
    current = "X"
    for b in buttons:
        b.config(text="")
    result_label.config(text="")
    update_score()
    update_turn()

def update_score():
    score_label.config(
        text=f"❌ {p1_name}: {score_x}    ⭕ {p2_name}: {score_o}    🤝 {score_draw}"
    )

def update_turn():
    left_player.config(fg=NEON_X if current=="X" else MUTED)
    right_player.config(fg=NEON_O if current=="O" else MUTED)

def intro_screen():
    clear()

    frame = tk.Frame(root, bg=BG)
    frame.pack(expand=True)

    tk.Label(frame, text="TIC TAC TOE",
        font=("Arial Black", 46),
        fg=NEON_O, bg=BG).pack(pady=20)

    tk.Label(frame, text="Strategy Based Neon Game",
        font=("Arial",18),
        fg=TEXT, bg=BG).pack()

    tk.Label(frame,
        text="Play with friends or challenge AI\n"
             "Includes history & settings\n"
             "Smooth neon UI experience",
        font=("Arial",14),
        fg=MUTED, bg=BG,
        justify="center").pack(pady=20)

    tk.Button(frame, text="START ▶",
        bg=BTN_BG, fg=TEXT,
        width=18, height=2,
        font=("Arial",16),
        command=mode_screen).pack(pady=40)


def mode_screen():
    clear()
    selected = ""

    def choose(m):
        nonlocal selected
        selected = m
        mp_btn.config(bg=NEON_O if m=="PVP" else BTN_BG)
        ai_btn.config(bg=NEON_O if m=="AI" else BTN_BG)

    def next_page():
        if selected:
            global game_mode
            game_mode = selected
            name_screen()

    tk.Label(root, text="SELECT GAME MODE",
        font=("Arial Black",32),
        fg=NEON_O,bg=BG).pack(pady=40)

    mp_btn = tk.Button(root, text="👥 MULTIPLAYER",
        bg=BTN_BG, fg=TEXT,
        width=24, height=2,
        font=("Arial",18),
        command=lambda: choose("PVP"))
    mp_btn.pack(pady=15)

    ai_btn = tk.Button(root, text="🤖 VS COMPUTER",
        bg=BTN_BG, fg=TEXT,
        width=24, height=2,
        font=("Arial",18),
        command=lambda: choose("AI"))
    ai_btn.pack(pady=15)

    tk.Button(root, text="NEXT ▶",
        bg=BTN_BG, fg=TEXT,
        width=14,
        font=("Arial",14),
        command=next_page).pack(pady=30)

def name_screen():
    clear()

    frame = tk.Frame(root, bg=PANEL_BG)
    frame.pack(pady=100)

    tk.Label(frame, text="ENTER PLAYER NAMES",
        font=("Arial Black",26),
        fg=NEON_O, bg=PANEL_BG).pack(pady=20)

    tk.Label(frame, text="PLAYER ❌ NAME",
        fg=TEXT, bg=PANEL_BG,
        font=("Arial",16)).pack()

    p1 = tk.Entry(frame, font=("Arial",18))
    p1.pack(pady=10)

    if game_mode == "PVP":
        tk.Label(frame, text="PLAYER ⭕ NAME",
            fg=TEXT, bg=PANEL_BG,
            font=("Arial",16)).pack()
        p2 = tk.Entry(frame, font=("Arial",18))
        p2.pack(pady=10)

    def start_game():
        name1 = p1.get().strip()
        name2 = "AI BOT" if game_mode=="AI" else p2.get().strip()

        if not name1 or (game_mode=="PVP" and not name2):
            if not messagebox.askyesno(
                "Confirm",
                "Name not entered.\nContinue with default names?"
            ):
                return
        globals()["p1_name"] = name1 or "Player 1"
        globals()["p2_name"] = name2 or "Player 2"
        game_screen()

    tk.Button(frame, text="START GAME ▶",
        bg=BTN_BG, fg=TEXT,
        width=18,
        font=("Arial",16),
        command=start_game).pack(pady=30)
def settings_screen():
    clear()

    def toggle_sound():
        global sound_on
        sound_on = not sound_on
        sound_btn.config(text=f"SOUND : {'ON' if sound_on else 'OFF'}")

    def reset_scores():
        global score_x, score_o, score_draw
        score_x = score_o = score_draw = 0
        messagebox.showinfo("Reset", "Scores Reset Successfully")

    tk.Label(root, text="SETTINGS",
        font=("Arial Black",36),
        fg=NEON_O, bg=BG).pack(pady=40)

    sound_btn = tk.Button(root,
        text=f"SOUND : {'ON' if sound_on else 'OFF'}",
        bg=BTN_BG, fg=TEXT,
        width=20,
        font=("Arial",18),
        command=toggle_sound)
    sound_btn.pack(pady=20)

    tk.Button(root, text="RESET SCORES",
        bg=BTN_BG, fg=TEXT,
        width=20,
        font=("Arial",18),
        command=reset_scores).pack(pady=20)

    tk.Button(root, text="◀ BACK",
        bg=BTN_BG, fg=TEXT,
        width=16,
        font=("Arial",16),
        command=game_screen).pack(pady=40)
def history_screen():
    clear()

    tk.Label(root, text="MATCH HISTORY",
        font=("Arial Black",34),
        fg=NEON_O, bg=BG).pack(pady=20)

    box = tk.Listbox(root,
        width=70,
        height=12,
        font=("Consolas",14),
        bg=PANEL_BG,
        fg=TEXT)
    box.pack(pady=20)

    if history:
        for h in history:
            box.insert(tk.END, h)
    else:
        box.insert(tk.END, "No matches played yet.")

    tk.Button(root, text="◀ BACK",
        bg=BTN_BG, fg=TEXT,
        width=14,
        font=("Arial",14),
        command=game_screen).pack(pady=30)
def game_screen():
    global left_player, right_player, score_label, result_label
    buttons.clear()
    clear()

    score_label = tk.Label(root, fg=TEXT, bg=BG, font=("Arial",16))
    score_label.pack(pady=10)
    update_score()

    main = tk.Frame(root, bg=BG)
    main.pack(expand=True)

    left_player = tk.Label(main,
        text=f"❌\n{p1_name}",
        fg=NEON_X, bg=BG,
        font=("Arial Black",24))
    left_player.pack(side="left", padx=40)

    grid = tk.Frame(main, bg=BG)
    grid.pack(side="left")

    for i in range(9):
        b = tk.Button(grid,
            bg=BTN_BG,
            font=("Arial Black",36),
            width=4, height=2,
            command=lambda i=i: click(i))
        b.grid(row=i//3, column=i%3, padx=12, pady=12)
        buttons.append(b)

    right_player = tk.Label(main,
        text=f"⭕\n{p2_name}",
        fg=NEON_O, bg=BG,
        font=("Arial Black",24))
    right_player.pack(side="right", padx=40)

    result_label = tk.Label(root, bg=BG, font=("Arial Black",22))
    result_label.pack(pady=10)

    ctrl = tk.Frame(root, bg=BG)
    ctrl.pack(pady=10)

    tk.Button(ctrl, text="BACK",
        bg=BTN_BG, fg=TEXT,
        width=12,
        font=("Arial",14),
        command=mode_screen).pack(side="left", padx=8)

    tk.Button(ctrl, text="SETTINGS",
        bg=BTN_BG, fg=TEXT,
        width=12,
        font=("Arial",14),
        command=settings_screen).pack(side="left", padx=8)

    tk.Button(ctrl, text="HISTORY",
        bg=BTN_BG, fg=TEXT,
        width=12,
        font=("Arial",14),
        command=history_screen).pack(side="left", padx=8)

    tk.Button(ctrl, text="EXIT",
        bg=BTN_BG, fg=TEXT,
        width=12,
        font=("Arial",14),
        command=root.destroy).pack(side="left", padx=8)

    update_turn()
intro_screen()
root.mainloop()
