import customtkinter as ctk
import pyautogui
import time
import threading
import os

# Настройка внешнего вида окна
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AutoAcceptApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.title("Dota 2 Auto Accept")
        self.geometry("300x200")
        self.resizable(False, False)
        self.attributes('-topmost', True)

        # Путь к изображению (автоматически определяет папку со скриптом)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.script_dir, 'accept_button.png')

        self.is_running = False

        # --- ЭЛЕМЕНТЫ ИНТЕРФЕЙСА ---
        self.title_label = ctk.CTkLabel(self, text="Dota 2 Auto Accept", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=(15, 5))

        self.status_label = ctk.CTkLabel(self, text="Статус: Остановлен", text_color="gray")
        self.status_label.pack(pady=(0, 15))

        self.start_btn = ctk.CTkButton(self, text="СТАРТ", fg_color="green", hover_color="darkgreen",
                                       command=self.start_bot)
        self.start_btn.pack(pady=5)

        self.stop_btn = ctk.CTkButton(self, text="СТОП", fg_color="red", hover_color="darkred", state="disabled",
                                      command=self.stop_bot)
        self.stop_btn.pack(pady=5)

    def start_bot(self):
        self.is_running = True
        self.status_label.configure(text="Статус: Поиск матча...", text_color="yellow")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        threading.Thread(target=self.bot_loop, daemon=True).start()

    def stop_bot(self):
        self.is_running = False
        self.status_label.configure(text="Статус: Остановлен", text_color="gray")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def bot_loop(self):
        while self.is_running:
            try:
                # Используем переменный путь image_path
                button = pyautogui.locateCenterOnScreen(self.image_path, confidence=0.6)

                if button is not None:
                    self.status_label.configure(text="Матч найден! Принимаю...", text_color="#00FF00")
                    pyautogui.click(button)
                    time.sleep(10)

                    if self.is_running:
                        self.status_label.configure(text="Статус: Поиск матча...", text_color="yellow")

            except Exception as e:
                # Если файл не найден или ошибка OpenCV, выведем в консоль для отладки
                # print(f"Ошибка: {e}")
                pass

            time.sleep(1)


if __name__ == "__main__":
    app = AutoAcceptApp()
    app.mainloop()