import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import os

def load_words():
    filename = 'words.txt'
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Україна\nБорщ\nКава\nПрограмування\n")
        return ["Україна", "Борщ", "Кава", "Програмування"]
    with open(filename, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f.readlines() if line.strip()]
    return words if words else ["Кіт", "Сонце", "Київ"]

def save_new_word(word):
    with open('words.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n{word}")

class AliasUltimate:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.show_welcome_screen()

    def show_welcome_screen(self):
        welcome = tk.Toplevel(self.root)
        welcome.title("WEZAXES ENTERTAINMENT")
        welcome.geometry("450x300")
        welcome.configure(bg='#11111b')
        welcome.resizable(False, False)

        tk.Label(welcome, text="WEZAXES ENTERTAINMENT", font=("Courier New", 14, "bold"), 
                 bg='#11111b', fg='#fab387').pack(pady=10)
        
        tk.Label(welcome, text="УВАГА!", font=("Segoe UI", 24, "bold"), 
                 bg='#11111b', fg='#f38ba8').pack()
        
        tk.Label(welcome, text="Це СУПЕР пробна версія.\nСлова і все інше ше буде\nдопрацьовуватись.", 
                 font=("Segoe UI", 13), bg='#11111b', fg='#cdd6f4', justify="center").pack(pady=10)

        def close_welcome():
            welcome.destroy()
            self.root.deiconify()
            self.start_initialization()

        tk.Button(welcome, text="ЛАДНО", font=("Segoe UI", 12, "bold"), 
                  bg='#89b4fa', fg='#11111b', width=20, height=2, 
                  command=close_welcome).pack(pady=15)

    def start_initialization(self):
        self.all_words = load_words()
        self.teams = []
        self.scores = {}
        self.current_team_idx = 0
        self.current_round = 1
        self.timer_running = False
        self.setup_game()

    def setup_game(self):
        self.root.title("Alias - Wezaxes Edition")
        self.root.geometry("500x750")
        self.root.configure(bg='#1e1e2e')

        n_teams = simpledialog.askinteger("Старт", "Скільки команд?", minvalue=2, maxvalue=6) or 2
        for i in range(n_teams):
            name = simpledialog.askstring("Команди", f"Назва команди {i+1}:") or f"Команда {i+1}"
            self.teams.append(name)
            self.scores[name] = 0

        self.total_rounds = simpledialog.askinteger("Раунди", "Кількість раундів:", minvalue=1) or 3
        self.round_duration = simpledialog.askinteger("Час", "Секунд на раунд:", minvalue=5) or 60
        
        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        # Інфо панель
        self.info_label = tk.Label(self.root, text="", font=("Segoe UI", 14, "bold"), bg='#1e1e2e', fg='#cdd6f4')
        self.info_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="--", font=("Consolas", 30, "bold"), bg='#1e1e2e', fg='#f38ba8')
        self.timer_label.pack()

        # Поле слова
        self.word_frame = tk.Frame(self.root, bg='#313244', height=150)
        self.word_frame.pack(pady=10, padx=30, fill="x")
        self.word_frame.pack_propagate(False) # Щоб фрейм не стискався під текст
        
        self.word_label = tk.Label(self.word_frame, text="ГОТОВІ?", font=("Segoe UI", 32, "bold"), 
                                  bg='#313244', fg='#f9e2af', wraplength=400)
        self.word_label.pack(expand=True)

        # Великі кнопки (Вертикальні)
        self.game_btns_frame = tk.Frame(self.root, bg='#1e1e2e')
        self.game_btns_frame.pack(pady=10, padx=30, fill="x")

        self.ok_btn = tk.Button(self.game_btns_frame, text="ВГАДАНО ✅", font=("Segoe UI", 20, "bold"), 
                               bg='#a6e3a1', fg='#11111b', height=3, command=self.word_guessed, state="disabled")
        self.ok_btn.pack(fill="x", pady=5)

        self.skip_btn = tk.Button(self.game_btns_frame, text="СКІП ❌", font=("Segoe UI", 20, "bold"), 
                                 bg='#f38ba8', fg='#11111b', height=3, command=self.word_skipped, state="disabled")
        self.skip_btn.pack(fill="x", pady=5)

        # Кнопка СТАРТ
        self.start_btn = tk.Button(self.root, text="ПОЧАТИ РАУНД", font=("Segoe UI", 16, "bold"), 
                                  bg='#89b4fa', fg='#11111b', height=2, command=self.start_round)
        self.start_btn.pack(pady=15, padx=30, fill="x")

        # Кнопка Додати слово
        self.add_word_btn = tk.Button(self.root, text="+ Додати нове слово в базу", font=("Segoe UI", 10), 
                                     bg='#45475a', fg='#cdd6f4', bd=0, command=self.add_custom_word)
        self.add_word_btn.pack(side="bottom", pady=10)

    def add_custom_word(self):
        new_w = simpledialog.askstring("Словник", "Введіть нове слово:")
        if new_w:
            save_new_word(new_w)
            self.all_words.append(new_w)
            messagebox.showinfo("Wezaxes Cloud", f"Слово '{new_w}' додано до бази!")

    def update_ui(self):
        team = self.teams[self.current_team_idx]
        self.info_label.config(text=f"РАУНД {self.current_round}/{self.total_rounds}\nКОМАНДА: {team.upper()}")

    def start_round(self):
        self.time_left = self.round_duration
        self.timer_running = True
        self.start_btn.config(state="disabled", bg="#45475a")
        self.ok_btn.config(state="normal")
        self.skip_btn.config(state="normal")
        self.next_word()
        self.tick()

    def tick(self):
        if self.time_left > 0 and self.timer_running:
            self.timer_label.config(text=f"{self.time_left:02d}")
            self.time_left -= 1
            self.root.after(1000, self.tick)
        elif self.time_left == 0:
            self.end_round()

    def next_word(self):
        if self.all_words:
            self.current_word = random.choice(self.all_words)
            self.word_label.config(text=self.current_word.upper())
        else:
            messagebox.showwarning("Wezaxes", "Слова закінчилися!")
            self.end_round()

    def word_guessed(self):
        self.scores[self.teams[self.current_team_idx]] += 1
        if self.current_word in self.all_words:
            self.all_words.remove(self.current_word)
        self.next_word()

    def word_skipped(self):
        self.scores[self.teams[self.current_team_idx]] -= 1
        self.next_word()

    def end_round(self):
        self.timer_running = False
        self.ok_btn.config(state="disabled")
        self.skip_btn.config(state="disabled")
        self.start_btn.config(state="normal", bg="#89b4fa")
        self.word_label.config(text="ЧАС ВИЙШОВ")
        
        current_team = self.teams[self.current_team_idx]
        
        if self.current_team_idx < len(self.teams) - 1:
            self.current_team_idx += 1
        else:
            self.current_team_idx = 0
            self.current_round += 1
        
        if self.current_round > self.total_rounds:
            self.show_winner()
        else:
            res_text = f"Команда {current_team} тепер має {self.scores[current_team]} балів.\n\nНаступні: {self.teams[self.current_team_idx]}"
            messagebox.showinfo("Кінець раунду", res_text)
            self.update_ui()

    def show_winner(self):
        res = "ФІНАЛЬНИЙ РАХУНОК WEZAXES:\n\n"
        sorted_res = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        for t, s in sorted_res:
            res += f"{t}: {s} балів\n"
        messagebox.showinfo("Гра закінчена", res)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AliasUltimate(root)
    root.mainloop()
