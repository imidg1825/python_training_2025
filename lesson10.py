import random
import tkinter as tk
from tkinter import messagebox

class MiniRPG:
    def __init__(self, root):
        self.root = root
        self.root.title("Мини-RPG")
        self.root.geometry("600x400")

        # переменные игры
        self.name = ""
        self.player_hp = 10
        self.player_potion = False
        self.monster_hp = 8
        self.attempt = 1

        # интерфейс
        self.label = tk.Label(root, text="Добро пожаловать в мини-RPG!", font=("Arial", 14))
        self.label.pack(pady=20)

        self.entry_label = tk.Label(root, text="Как тебя зовут, герой?", font=("Arial", 12))
        self.entry_label.pack()

        self.name_entry = tk.Entry(root, font=("Arial", 12))
        self.name_entry.pack(pady=10)

        self.start_button = tk.Button(root, text="Начать игру", command=self.start_game, font=("Arial", 12))
        self.start_button.pack(pady=10)

    def start_game(self):
        self.name = self.name_entry.get()
        if not self.name:
            messagebox.showwarning("Ошибка", "Введите имя!")
            return

        self.clear_window()
        self.label = tk.Label(self.root, text=f"Привет, {self.name}!", font=("Arial", 14))
        self.label.pack(pady=10)

        self.info_label = tk.Text(self.root, height=10, width=70, state="disabled", font=("Arial", 10))
        self.info_label.pack(pady=10)

        self.choice_frame = tk.Frame(self.root)
        self.choice_frame.pack(pady=10)

        self.choice1_btn = tk.Button(self.choice_frame, text="Пойти налево (тусклый коридор)", command=lambda: self.make_choice(1))
        self.choice1_btn.pack(side="left", padx=10)

        self.choice2_btn = tk.Button(self.choice_frame, text="Пойти направо (коридор с факелами)", command=lambda: self.make_choice(2))
        self.choice2_btn.pack(side="left", padx=10)

        self.update_info("Ты заходишь в старое подземелье. Впереди развилка: ЛЕВО и ПРАВО.\nТвоя задача — выжить и победить монстра.\n")

    def make_choice(self, choice):
        self.clear_window()
        self.choice_frame.destroy()

        if choice == 1:
            self.player_potion = True
            self.update_info("Ты осторожно идёшь по тёмному коридору...\nНатыкаешься на старый сундук и находишь ЗЕЛЬЕ ЛЕЧЕНИЯ! (+3 HP)\n")
        elif choice == 2:
            self.update_info("Ты идёшь по освещённому коридору.\nЗдесь безопасно, но ничего полезного нет.\n")
        else:
            self.update_info("Ты долго сомневался и в итоге пошёл прямо...\nК сожалению, это тупик. Приходится вернуться обратно.\nПока ты метался, монстр сам тебя нашёл.\n")

        self.update_info("Перед тобой появляется МОНСТР-СТРАЖНИК!\nБой начинается!\n")
        self.battle_screen()

    def battle_screen(self):
        self.clear_window()

        self.battle_info = tk.Text(self.root, height=12, width=70, state="disabled", font=("Arial", 10))
        self.battle_info.pack(pady=10)

        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(pady=10)

        self.attack_btn = tk.Button(self.action_frame, text="Удар мечом", command=lambda: self.player_action(1))
        self.attack_btn.pack(side="left", padx=5)

        self.defend_btn = tk.Button(self.action_frame, text="Защита", command=lambda: self.player_action(2))
        self.defend_btn.pack(side="left", padx=5)

        if self.player_potion:
            self.potion_btn = tk.Button(self.action_frame, text="Выпить зелье", command=lambda: self.player_action(3))
            self.potion_btn.pack(side="left", padx=5)

        self.run_btn = tk.Button(self.action_frame, text="Попробовать убежать", command=lambda: self.player_action(0))
        self.run_btn.pack(side="left", padx=5)

        self.update_battle_info()

    def player_action(self, action):
        if action == 1:  # атака
            damage = random.randint(2, 4)
            self.monster_hp -= damage
            self.update_battle_info(f"Ты бьёшь мечом и наносишь {damage} урона!\n")

        elif action == 2:  # защита
            self.update_battle_info("Ты поднимаешь щит и готовишься к удару.\n")

        elif action == 3 and self.player_potion:  # зелье
            self.player_hp += 3
            self.player_potion = False
            self.update_battle_info("Ты выпиваешь зелье. +3 к здоровью!\n")
            self.potion_btn.config(state="disabled")

        elif action == 0:  # убегаем
            escape_chance = random.randint(1, 4)
            if escape_chance == 1:
                self.update_battle_info("Тебе чудом удаётся убежать от монстра!\nИгра окончена. Ты выжил, но монстр остался в подземелье.\n")
                self.end_game()
                return
            else:
                self.update_battle_info("Не получилось убежать! Монстр перегородил дорогу.\n")

        else:
            self.update_battle_info("Ты мешкаешь и ничего полезного не делаешь...\n")

        if self.monster_hp <= 0:
            self.update_battle_info("\nМонстр повержен! Ты победил!\n")
            self.end_game()
            return

        # ход монстра
        self.monster_turn(action)

    def monster_turn(self, player_action):
        if player_action == 2:
            monster_damage = random.randint(0, 2)
            self.update_battle_info("Ты в защите, часть удара блокирована.\n")
        else:
            monster_damage = random.randint(1, 4)

        self.player_hp -= monster_damage
        self.update_battle_info(f"Монстр наносит тебе {monster_damage} урона!\n")

        if self.player_hp <= 0:
            self.update_battle_info("\nТвоё здоровье упало до нуля.\nМонстр победил... Но ты можешь запустить игру снова и отомстить!\n")
            self.end_game()
        else:
            self.attempt += 1
            self.update_battle_info(f"\nХод номер {self.attempt}\n")
            self.update_battle_info()

    def update_battle_info(self, text=""):
        self.battle_info.config(state="normal")
        self.battle_info.insert(tk.END, text)
        self.battle_info.config(state="disabled")
        self.battle_info.see(tk.END)

    def update_info(self, text):
        self.info_label.config(state="normal")
        self.info_label.insert(tk.END, text)
        self.info_label.config(state="disabled")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def end_game(self):
        self.clear_window()
        result_label = tk.Label(self.root, text="Игра завершена. Спасибо за игру!", font=("Arial", 14))
        result_label.pack(pady=20)

        if self.player_hp > 0 and self.monster_hp <= 0:
            win_label = tk.Label(self.root, text=f"Поздравляю, {self.name}!", font=("Arial", 12), fg="green")
            win_label.pack()
            win2_label = tk.Label(self.root, text="Ты очистил подземелье от монстра и вышел на свет героем!", font=("Arial", 12), fg="green")
            win2_label.pack()

root = tk.Tk()
game = MiniRPG(root)
root.mainloop()