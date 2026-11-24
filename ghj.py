import tkinter as tk
from tkinter import messagebox
import random
THEMES = {
    "Cartoon 🎈": {
        "bg": "#FFD700",       
        "fg": "#000000",     
        "button_bg": "#FF69B4", 
        "button_active": "#FF1493",
        "grid_bg": "#FFFACD",  # Lemon Chiffon
        "x_color": "#0000CD",  # Medium Blue
        "o_color": "#FF4500",  # Orange Red
        "font_large": ('Comic Sans MS', 50, 'bold'),
        "font_medium": ('Comic Sans MS', 20),
        "settings_icon": "⚙️",
    },
    "Forest 🍄": {
        "bg": "#1B4D3E",       # Deep Forest Green
        "fg": "#FFFFFF",       # White
        "button_bg": "#2E8B57", # Sea Green
        "button_active": "#228B22",
        "grid_bg": "#355E3B",  # Hunter Green
        "x_color": "#FFD700",  
        "o_color": "#98FB98", 
        "font_large": ('Georgia', 50, 'bold'),
        "font_medium": ('Georgia', 20),
        "settings_icon": "🌲",
    },
    "Cyber 💾": {
        "bg": "#000000",
        "fg": "#00ff41",       
        "button_bg": "#00aaff", 
        "button_active": "#0066cc",
        "grid_bg": "#1a1a1a",
        "x_color": "#ff00e6", 
        "o_color": "#00fffb", 
        "font_large": ('Consolas', 50, 'bold'),
        "font_medium": ('Consolas', 20),
        "settings_icon": "🌇",
    },
}

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("🎮 Ultimate Tic-Tac-Toe 🎮")
        
        # --- Fullscreen Configuration ---
        self.master.attributes('-fullscreen', True)
        self.master.bind('<Escape>', lambda e: self.master.attributes('-fullscreen', False))
        
        self.current_theme_name = "Cartoon 🎈"
        self.current_theme = THEMES[self.current_theme_name]
        
        # Game State
        self.game_mode = None     # 'single' or 'multi'
        self.ai_difficulty = 'Easy'
        self.game_over = False
        self.player_names = {'X': 'Player 1', 'O': 'Player 2'}

        self.board = [''] * 9
        self.current_player = 'X'
        self.buttons = []
        
        # Main container
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill='both')

        self.show_main_menu()
    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        self.current_theme = THEMES[theme_name]
        theme = self.current_theme

        self.master.config(bg=theme["bg"])
        self.main_frame.config(bg=theme["bg"])

        def style_widget(widget):
            try: widget.config(bg=theme["bg"])
            except: pass
            
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry)):
                try: widget.config(fg=theme["fg"])
                except: pass
                
                if isinstance(widget, tk.Button):
                     widget.config(bg=theme["button_bg"], activebackground=theme["button_active"], 
                                   font=theme["font_medium"])
                
                # Style Entry widgets specifically
                if isinstance(widget, tk.Entry):
                    widget.config(bg=theme["grid_bg"], font=theme["font_medium"], insertbackground=theme["fg"])

            for child in widget.winfo_children():
                style_widget(child)

        style_widget(self.main_frame)

        # Specific Overrides
        if hasattr(self, 'settings_button'):
             self.settings_button.config(
                text=theme["settings_icon"],
                bg=theme["button_bg"], activebackground=theme["button_active"],
                fg=theme["fg"], font=(theme["font_medium"][0], 25), width=4
            )
        
        if hasattr(self, 'status_label'):
            self.status_label.config(font=theme["font_medium"], bg=theme["bg"], fg=theme["fg"])

        # Grid Buttons
        for i, btn in enumerate(self.buttons):
            btn.config(bg=theme["grid_bg"], activebackground=theme["button_active"], font=theme["font_large"])
            if self.board[i] == 'X': btn.config(fg=theme["x_color"])
            elif self.board[i] == 'O': btn.config(fg=theme["o_color"])
            else: btn.config(fg=theme["fg"])

    def open_settings_popup(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("🎨 Settings")
        settings_window.geometry("500x350")
        settings_window.grab_set() 
        
        def select_theme(name):
            settings_window.config(bg=THEMES[name]["bg"])
            # Update popup widgets
            for w in settings_window.winfo_children():
                try: w.config(bg=THEMES[name]["bg"], fg=THEMES[name]["fg"])
                except: pass
                if isinstance(w, tk.Button): w.config(bg=THEMES[name]["button_bg"])
            self.apply_theme(name)
            
        settings_window.config(bg=self.current_theme["bg"])
        tk.Label(settings_window, text="✨ Pick Your Vibe! ✨", font=self.current_theme["font_medium"],
                 bg=self.current_theme["bg"], fg=self.current_theme["fg"]).pack(pady=20)

        for name in THEMES.keys():
            tk.Button(settings_window, text=name, command=lambda n=name: select_theme(n),
                      bg=self.current_theme["button_bg"], fg=self.current_theme["fg"],
                      font=self.current_theme["font_medium"]).pack(pady=10, padx=50, fill='x')
        
        tk.Button(settings_window, text="✅ Close", command=settings_window.destroy,
                  font=self.current_theme["font_medium"], bg=self.current_theme["button_bg"], fg=self.current_theme["fg"]).pack(pady=10)


    # --- 🏠 Menu & Layouts 🏠 ---
    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def add_top_bar(self):
        top_frame = tk.Frame(self.main_frame, bg=self.current_theme["bg"])
        top_frame.pack(fill='x', padx=30, pady=30)
        
        self.status_label = tk.Label(top_frame, text="", anchor='w',
                                     bg=self.current_theme["bg"], fg=self.current_theme["fg"],
                                     font=self.current_theme["font_medium"])
        self.status_label.pack(side='left', fill='x', expand=True)

        self.settings_button = tk.Button(top_frame, text=self.current_theme["settings_icon"],
                                         command=self.open_settings_popup,
                                         bg=self.current_theme["button_bg"], fg=self.current_theme["fg"],
                                         font=(self.current_theme["font_medium"][0], 25),
                                         width=4, borderwidth=0, relief=tk.FLAT)
        self.settings_button.pack(side='right')

    def add_bottom_bar(self):
        bottom_frame = tk.Frame(self.main_frame, bg=self.current_theme["bg"])
        bottom_frame.pack(side='bottom', fill='x', padx=30, pady=30)
        
        tk.Button(bottom_frame, text="🏠 Back to Menu ⬅️", command=self.show_main_menu,
                  bg=self.current_theme["button_bg"], fg=self.current_theme["fg"],
                  font=self.current_theme["font_medium"], borderwidth=0, relief=tk.FLAT
                  ).pack(side='left')

    def show_main_menu(self):
        self.clear_screen()
        self.add_top_bar()
        
        menu_frame = tk.Frame(self.main_frame, bg=self.current_theme["bg"])
        menu_frame.pack(expand=True, padx=100, pady=20)

        self.status_label.config(text="👋 Welcome! Let's play! 🎲")

        tk.Label(menu_frame, text="🚀 Ultimate X & O 🎮", font=(self.current_theme["font_large"][0], 60, 'bold'),
                 bg=self.current_theme["bg"], fg=self.current_theme["fg"]).pack(pady=40)
        
        tk.Button(menu_frame, text="👤 Single Player (vs AI 🤖)", 
                  command=self.show_difficulty_popup,
                  width=30, font=self.current_theme["font_medium"],
                  bg=self.current_theme["button_bg"], fg=self.current_theme["fg"]).pack(pady=15)

        tk.Button(menu_frame, text="👥 Multiplayer (vs Friend 🗣️)", 
                  command=self.show_names_popup,
                  width=30, font=self.current_theme["font_medium"],
                  bg=self.current_theme["button_bg"], fg=self.current_theme["fg"]).pack(pady=15)
        
        tk.Button(menu_frame, text="🚪 Exit Game ❌", 
                  command=self.master.quit,
                  width=30, font=self.current_theme["font_medium"],
                  bg=self.current_theme["button_bg"], fg=self.current_theme["fg"]).pack(pady=15)
        
        self.apply_theme(self.current_theme_name)

    # --- 📝 Popups: Difficulty & Names ---
    def show_difficulty_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("🤔 Select Difficulty")
        popup.geometry("400x400")
        popup.grab_set()

        # Apply basic theme to popup background
        popup.config(bg=self.current_theme["bg"])
        
        tk.Label(popup, text="🧠 How smart is the AI? 🤖", font=self.current_theme["font_medium"],
                 bg=self.current_theme["bg"], fg=self.current_theme["fg"]).pack(pady=20)

        def set_ai(difficulty):
            self.ai_difficulty = difficulty
            self.player_names = {'X': 'You', 'O': f'AI ({difficulty})'} # Auto names
            popup.destroy()
            self.setup_game('single')

        difficulties = [("👶 Easy Peasy", 'Easy'), ("🧑‍🏫 Medium Rare", 'Medium'), ("🔥 Super Hard!", 'Hard')]
        for text, mode in difficulties:
            tk.Button(popup, text=text, command=lambda d=mode: set_ai(d),
                      bg=self.current_theme["button_bg"], activebackground=self.current_theme["button_active"],
                      fg=self.current_theme["fg"], font=self.current_theme["font_medium"], width=20).pack(pady=10)

    def show_names_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("📝 Enter Player Names")
        popup.geometry("500x400")
        popup.grab_set()
        popup.config(bg=self.current_theme["bg"])

        tk.Label(popup, text="🗣️ Who is playing?", font=self.current_theme["font_medium"],
                 bg=self.current_theme["bg"], fg=self.current_theme["fg"]).pack(pady=20)

        # Player 1 Input
        tk.Label(popup, text="Player 1 (X) Name:", font=(self.current_theme["font_medium"][0], 14),
                 bg=self.current_theme["bg"], fg=self.current_theme["fg"]).pack(pady=5)
        entry_p1 = tk.Entry(popup, font=self.current_theme["font_medium"], justify='center')
        entry_p1.insert(0, "Player 1")
        entry_p1.pack(pady=5)

        # Player 2 Input
        tk.Label(popup, text="Player 2 (O) Name:", font=(self.current_theme["font_medium"][0], 14),
                 bg=self.current_theme["bg"], fg=self.current_theme["fg"]).pack(pady=5)
        entry_p2 = tk.Entry(popup, font=self.current_theme["font_medium"], justify='center')
        entry_p2.insert(0, "Player 2")
        entry_p2.pack(pady=5)

        def start_multi():
            p1 = entry_p1.get().strip() or "Player 1"
            p2 = entry_p2.get().strip() or "Player 2"
            self.player_names = {'X': p1, 'O': p2}
            popup.destroy()
            self.setup_game('multi')

        tk.Button(popup, text="🚀 Start Game", command=start_multi,
                  bg=self.current_theme["button_bg"], activebackground=self.current_theme["button_active"],
                  fg=self.current_theme["fg"], font=self.current_theme["font_medium"], width=20).pack(pady=30)
        
        # Apply theme colors to the new entries
        entry_p1.config(bg=self.current_theme["grid_bg"], fg=self.current_theme["fg"])
        entry_p2.config(bg=self.current_theme["grid_bg"], fg=self.current_theme["fg"])


    # --- 🏆 Game Over Popup 🏆 ---
    def show_game_over_popup(self, message, title):
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.geometry("550x350")
        popup.grab_set()
        popup.config(bg=self.current_theme["bg"])
        
        tk.Label(popup, text=message, font=(self.current_theme["font_large"][0], 30, 'bold'),
                 bg=self.current_theme["bg"], fg=self.current_theme["fg"], wraplength=500).pack(pady=40)
        
        btn_frame = tk.Frame(popup, bg=self.current_theme["bg"])
        btn_frame.pack(pady=20)

        def restart_action():
            popup.destroy()
            self.setup_game(self.game_mode)

        def menu_action():
            popup.destroy()
            self.show_main_menu()

        tk.Button(btn_frame, text="🔄 Play Again!", command=restart_action,
                  bg=self.current_theme["button_bg"], fg=self.current_theme["fg"],
                  font=self.current_theme["font_medium"], width=15).pack(side='left', padx=15)

        tk.Button(btn_frame, text="🏠 Main Menu", command=menu_action,
                  bg=self.current_theme["button_bg"], fg=self.current_theme["fg"],
                  font=self.current_theme["font_medium"], width=15).pack(side='left', padx=15)


    # --- 🎮 Game Setup ---
    def setup_game(self, mode):
        self.clear_screen()
        self.add_top_bar()
        self.add_bottom_bar()
        self.game_mode = mode
        self.board = [''] * 9
        self.current_player = 'X'
        self.buttons = []
        self.game_over = False
        
        self.update_status()

        # Game Board
        center_frame = tk.Frame(self.main_frame, bg=self.current_theme["bg"])
        center_frame.pack(expand=True)
        game_frame = tk.Frame(center_frame, bg=self.current_theme["bg"], bd=5, relief=tk.RIDGE)
        game_frame.pack(padx=20, pady=20)

        for i in range(9):
            row, col = divmod(i, 3)
            btn = tk.Button(game_frame, text='', font=self.current_theme["font_large"],
                            bg=self.current_theme["grid_bg"], activebackground=self.current_theme["button_active"],
                            fg=self.current_theme["fg"], width=5, height=2, 
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)
        
        self.apply_theme(self.current_theme_name)

    # --- 🧠 Game Logic ---
    def make_move(self, index):
        if self.board[index] == '' and not self.game_over:
            self.board[index] = self.current_player
            
            fg_color = self.current_theme["x_color"] if self.current_player == 'X' else self.current_theme["o_color"]
            self.buttons[index].config(text=self.current_player, fg=fg_color, state=tk.DISABLED)
            
            if self.check_winner():
                self.game_over = True
                winner_name = self.player_names[self.current_player]
                self.show_game_over_popup(f"🎉 {winner_name} Wins! 🏆", "🎊 Victory! 🎊")
                self.disable_all_buttons()
            elif '' not in self.board:
                self.game_over = True
                self.show_game_over_popup("🤝 It's a Draw! 😐", "🏁 Game Over 🏁")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.update_status()
                
                if self.game_mode == 'single' and self.current_player == 'O' and not self.game_over:
                    self.master.after(500, self.ai_move) 

    def ai_move(self):
        if self.game_over: return
        move = self.get_best_ai_move()
        if move is not None:
            self.make_move(move)

    def get_best_ai_move(self):
        available = [i for i, spot in enumerate(self.board) if spot == '']
        if not available: return None

        # 1. Win or Block
        for player in ['O', 'X']:
            for move in available:
                board_copy = list(self.board)
                board_copy[move] = player
                if self.check_win_simulation(board_copy, player):
                    if self.ai_difficulty in ['Medium', 'Hard'] or player == 'O':
                        return move
        # 2. Hard
        if self.ai_difficulty == 'Hard':
            if 4 in available: return 4
            corners = [i for i in [0, 2, 6, 8] if i in available]
            if corners: return random.choice(corners)
        # 3. Medium
        if self.ai_difficulty == 'Medium':
            if 4 in available: return 4
            
        return random.choice(available)

    def check_win_simulation(self, board, player):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if board[a] == board[b] == board[c] == player: return True
        return False

    def check_winner(self):
        if self.check_win_simulation(self.board, self.current_player):
            wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
            for a,b,c in wins:
                if self.board[a] == self.board[b] == self.board[c] == self.current_player:
                    for i in [a,b,c]: self.buttons[i].config(bg=self.current_theme["button_active"])
            return True
        return False

    def disable_all_buttons(self):
        for btn in self.buttons: btn.config(state=tk.DISABLED)

    def update_status(self):
        current_name = self.player_names[self.current_player]
        self.status_label.config(text=f"👉 Turn: {current_name} ({self.current_player})")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()