import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import pyautogui
import time
import webbrowser
import os
import subprocess
import threading
import sys
import winreg
import psutil
import pygame
from gtts import gTTS
import tempfile
import datetime
import locale

# Настройка русского языка для дат
try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
except:
    pass

# Настройка темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PeterElegantAssistant:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🌟 Питер - Умный Ассистент")
        self.root.geometry("1300x850")
        self.root.configure(fg_color="#0A0A15")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Инициализация голоса
        self.setup_female_voice()
        
        self.is_listening = True
        self.recognizer = sr.Recognizer()
        
        self.setup_beautiful_ui()
        self.start_always_listening()
        
    def setup_female_voice(self):
        """Настраивает женский голос"""
        try:
            self.use_online_tts = True
            pygame.mixer.init()
            self.engine = pyttsx3.init()
            
            # Ищем женский голос
            voices = self.engine.getProperty('voices')
            female_voices = [v for v in voices if any(name in v.name.lower() for name in ['female', 'zira', 'natalia', 'irina'])]
            
            if female_voices:
                self.engine.setProperty('voice', female_voices[0].id)
                print(f"🎀 Выбран женский голос: {female_voices[0].name}")
            
            # Нежные настройки голоса
            self.engine.setProperty('rate', 160)
            self.engine.setProperty('volume', 0.9)
            self.engine.setProperty('pitch', 115)
            
        except Exception as e:
            print(f"Ошибка инициализации голоса: {e}")

    def speak(self, text):
        """Произносит текст с подтверждением"""
        self.log_message(f"🌸 Питер: {text}")
        time.sleep(0.2)
        
        try:
            if self.use_online_tts:
                tts = gTTS(text=text, lang='ru', slow=False)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tts.save(tmp_file.name)
                    pygame.mixer.music.load(tmp_file.name)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                    os.unlink(tmp_file.name)
            else:
                self.engine.say(text)
                self.engine.runAndWait()
        except:
            self.engine.say(text)
            self.engine.runAndWait()

    def get_current_time_info(self):
        """Получает текущее время, дату и день недели"""
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%d %B %Y")
        day_str = now.strftime("%A")
        return time_str, date_str, day_str

    def setup_beautiful_ui(self):
        # Основной контейнер с градиентом
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # ЛЕВАЯ ПАНЕЛЬ - ПРИЛОЖЕНИЯ (полупрозрачная с размытием)
        left_panel = ctk.CTkFrame(
            main_container, 
            fg_color="#1A1A2E",  # Темный с прозрачностью
            width=320,
            corner_radius=25
        )
        left_panel.pack(side="left", fill="y", padx=(15, 10), pady=15)
        left_panel.pack_propagate(False)
        
        # Заголовок левой панели
        apps_title = ctk.CTkLabel(
            left_panel,
            text="🚀 БЫСТРЫЙ ЗАПУСК",
            font=("SF Pro Display", 22, "bold"),
            text_color="#FF6B9D"
        )
        apps_title.pack(pady=(30, 25))
        
        # Кнопки приложений на левой панели
        app_buttons = [
            ("🎮 Discord", self.launch_discord, "#5865F2"),
            ("🎯 Steam", self.launch_steam, "#000000"),
            ("🎨 SkinChanger", self.launch_skinchanger, "#FF6B9D"),
            ("🌐 Браузер", self.launch_browser, "#4285F4"),
            ("📺 YouTube", self.open_youtube, "#FF0000"),
            ("👥 ВКонтакте", self.open_vk, "#4C75A3"),
            ("📸 Скриншот", self.take_screenshot, "#FF6B6B"),
            ("🎵 Музыка", self.open_spotify, "#1DB954")
        ]
        
        for text, command, color in app_buttons:
            btn = ctk.CTkButton(
                left_panel,
                text=text,
                command=command,
                font=("SF Pro Display", 15),
                fg_color=color,
                hover_color=self.darken_color(color),
                width=280,
                height=50,
                corner_radius=20,
                border_width=2,
                border_color=self.lighten_color(color)
            )
            btn.pack(pady=8, padx=20)
        
        # Разделитель
        separator = ctk.CTkFrame(left_panel, height=3, fg_color="#333344", corner_radius=10)
        separator.pack(fill="x", pady=25, padx=25)
        
        # Системные команды на левой панели
        system_title = ctk.CTkLabel(
            left_panel,
            text="⚙️ СИСТЕМА",
            font=("SF Pro Display", 20, "bold"),
            text_color="#BB86FC"
        )
        system_title.pack(pady=(10, 20))
        
        system_buttons = [
            ("🖥️ Выключить ПК", self.shutdown_pc, "#FF6B6B"),
            ("🔃 Перезагрузить", self.restart_pc, "#FFA726"),
            ("💤 Спящий режим", self.sleep_pc, "#42A5F5"),
            ("🚫 Закрыть браузеры", self.close_browsers, "#EF5350"),
            ("🕐 Время и дата", self.speak_time_date, "#66BB6A")
        ]
        
        for text, command, color in system_buttons:
            btn = ctk.CTkButton(
                left_panel,
                text=text,
                command=command,
                font=("SF Pro Display", 13),
                fg_color=color,
                hover_color=self.darken_color(color),
                width=250,
                height=40,
                corner_radius=15
            )
            btn.pack(pady=6, padx=25)
        
        # ПРАВАЯ ПАНЕЛЬ - ОСНОВНОЙ ИНТЕРФЕЙС
        right_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        # Верхняя панель с информацией
        top_info = ctk.CTkFrame(right_panel, fg_color="#1E1E2E", corner_radius=25)
        top_info.pack(fill="x", pady=(0, 20))
        
        # Аватар и информация
        avatar_frame = ctk.CTkFrame(top_info, fg_color="transparent")
        avatar_frame.pack(pady=25, padx=30)
        
        # Аватар с анимацией
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="🌟",
            font=("Segoe UI Emoji", 45),
            text_color="#FF6B9D"
        )
        avatar_label.pack(side="left", padx=(0, 20))
        
        # Информация об ассистенте
        info_frame = ctk.CTkFrame(avatar_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text="Питер",
            font=("SF Pro Display", 28, "bold"),
            text_color="#FFFFFF"
        )
        name_label.pack(anchor="w")
        
        status_label = ctk.CTkLabel(
            info_frame,
            text="🔴 Всегда на связи • Готова помочь",
            font=("SF Pro Display", 16),
            text_color="#4CAF50"
        )
        status_label.pack(anchor="w", pady=(5, 0))
        
        # Текущее время и дата
        time_frame = ctk.CTkFrame(top_info, fg_color="#2A2D3E", corner_radius=15)
        time_frame.pack(pady=(0, 25), padx=30, fill="x")
        
        self.time_label = ctk.CTkLabel(
            time_frame,
            text="",
            font=("SF Pro Display", 14),
            text_color="#BB86FC"
        )
        self.time_label.pack(pady=12)
        self.update_time_display()
        
        # ОСНОВНОЙ КОНТЕНТ - Лог и команды
        content_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Лог диалога
        log_container = ctk.CTkFrame(content_frame, fg_color="#1E1E2E", corner_radius=25)
        log_container.pack(fill="both", expand=True)
        
        log_header = ctk.CTkLabel(
            log_container,
            text="💬 ДИАЛОГ С ПИТЕРОМ",
            font=("SF Pro Display", 18, "bold"),
            text_color="#FFFFFF"
        )
        log_header.pack(pady=20)
        
        self.log_text = ctk.CTkTextbox(
            log_container,
            fg_color="#0A0A15",
            text_color="#E0E0E0",
            font=("SF Pro Display", 13),
            corner_radius=20,
            border_width=2,
            border_color="#333344"
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Приветственное сообщение
        self.root.after(1000, self.welcome_message)

    def update_time_display(self):
        """Обновляет отображение времени"""
        time_str, date_str, day_str = self.get_current_time_info()
        self.time_label.configure(text=f"🕐 {time_str} • {date_str} • {day_str.capitalize()}")
        self.root.after(60000, self.update_time_display)  # Обновлять каждую минуту

    def darken_color(self, color):
        """Темнее цвет для hover эффекта"""
        if color.startswith("#"):
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            darkened = tuple(max(0, c - 40) for c in rgb)
            return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        return color

    def lighten_color(self, color):
        """Светлее цвет для border"""
        if color.startswith("#"):
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            lightened = tuple(min(255, c + 40) for c in rgb)
            return f"#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}"
        return color

    def welcome_message(self):
        welcome_text = """🌟 Добро пожаловать! Я Питер - ваш умный и элегантный ассистент.

✨ ЧТО Я УМЕЮ:

🎮 БЫСТРЫЙ ЗАПУСК:
• Discord, Steam, SkinChanger
• Браузер, YouTube, ВКонтакте
• Скриншоты, музыка

⚙️ СИСТЕМНЫЕ КОМАНДЫ:
• Управление питанием ПК
• Закрытие приложений
• Время и дата

🎤 ГОЛОСОВОЕ УПРАВЛЕНИЕ:
Просто говорите команды, и я выполню их!

Попробуйте сказать:
• "Привет Питер" - поздороваться
• "Открой YouTube" - запустить YouTube  
• "Какое время?" - узнать время
• "Выключи компьютер" - выключить ПК"""

        self.log_message(welcome_text)
        self.speak("Привет! Я Питер, ваш элегантный помощник. Готова помочь вам с любыми задачами!")

    def log_message(self, message):
        """Добавляет сообщение в лог"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n\n")
        self.log_text.see("end")
        self.root.update()

    # 🎮 МЕТОДЫ ЗАПУСКА ПРИЛОЖЕНИЙ
    def launch_discord(self):
        self.log_message("🎮 Запускаю Discord...")
        try:
            os.system("start discord:")
            self.speak("Сделано! Discord запущен")
            self.log_message("✅ Discord запущен")
        except Exception as e:
            self.log_message(f"❌ Ошибка: {e}")

    def launch_steam(self):
        self.log_message("🎮 Запускаю Steam...")
        try:
            os.system("start steam:")
            self.speak("Готово! Steam запущен")
            self.log_message("✅ Steam запущен")
        except Exception as e:
            self.log_message(f"❌ Ошибка: {e}")

    def launch_skinchanger(self):
        """Запуск SkinChanger"""
        self.log_message("🎨 Запускаю SkinChanger...")
        try:
            # Пробуем разные пути для SkinChanger
            paths = [
                "SkinChanger.exe",
                "skinchanger.exe", 
                r"C:\Program Files\SkinChanger\SkinChanger.exe",
                r"C:\Program Files (x86)\SkinChanger\SkinChanger.exe",
                os.path.expanduser("~") + r"\Desktop\SkinChanger.exe"
            ]
            
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    self.speak("Сделано! SkinChanger запущен")
                    self.log_message(f"✅ SkinChanger запущен: {path}")
                    return
            
            self.speak("SkinChanger не найден. Проверьте установку.")
            self.log_message("❌ SkinChanger не найден")
        except Exception as e:
            self.log_message(f"❌ Ошибка: {e}")

    def launch_browser(self):
        self.log_message("🌐 Открываю браузер...")
        webbrowser.open("https://google.com")
        self.speak("Готово! Браузер открыт")
        self.log_message("✅ Браузер открыт")

    def open_youtube(self):
        self.log_message("📺 Открываю YouTube...")
        webbrowser.open("https://youtube.com")
        self.speak("Сделано! YouTube открыт")
        self.log_message("✅ YouTube открыт")

    def open_vk(self):
        self.log_message("👥 Открываю ВКонтакте...")
        webbrowser.open("https://vk.com")
        self.speak("Готово! ВКонтакте открыт")
        self.log_message("✅ ВКонтакте открыт")

    def open_spotify(self):
        self.log_message("🎵 Запускаю музыку...")
        try:
            os.system("start spotify:")
            self.speak("Сделано! Музыкальный плеер запущен")
            self.log_message("✅ Музыкальный плеер запущен")
        except:
            webbrowser.open("https://open.spotify.com")
            self.speak("Готово! Spotify открыт в браузере")
            self.log_message("🌐 Spotify в браузере")

    def take_screenshot(self):
        self.log_message("📸 Делаю скриншот...")
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{int(time.time())}.png"
            screenshot.save(filename)
            self.speak("Сделано! Скриншот сохранён")
            self.log_message(f"✅ Скриншот: {filename}")
        except Exception as e:
            self.log_message(f"❌ Ошибка: {e}")

    # ⚙️ СИСТЕМНЫЕ КОМАНДЫ
    def shutdown_pc(self):
        self.speak("Выключаю компьютер через 10 секунд!")
        self.log_message("🖥️ Выключение ПК через 10 секунд...")
        os.system("shutdown /s /t 10")

    def restart_pc(self):
        self.speak("Перезагружаю компьютер через 10 секунд!")
        self.log_message("🔃 Перезагрузка ПК через 10 секунд...")
        os.system("shutdown /r /t 10")

    def sleep_pc(self):
        self.speak("Перевожу компьютер в спящий режим!")
        self.log_message("💤 Спящий режим...")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def close_browsers(self):
        self.speak("Закрываю все браузеры!")
        self.log_message("🚫 Закрываю браузеры...")
        try:
            browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe']
            for browser in browsers:
                os.system(f"taskkill /f /im {browser}")
            self.log_message("✅ Браузеры закрыты")
        except Exception as e:
            self.log_message(f"❌ Ошибка: {e}")

    def speak_time_date(self):
        """Произносит текущее время и дату"""
        time_str, date_str, day_str = self.get_current_time_info()
        message = f"Сейчас {time_str}. Сегодня {date_str}, {day_str}"
        self.speak(message)
        self.log_message(f"🕐 {message}")

    # 🎤 ГОЛОСОВОЕ УПРАВЛЕНИЕ
    def start_always_listening(self):
        def listen_loop():
            while self.is_listening:
                try:
                    command = self.listen()
                    if command and len(command) > 2:
                        self.process_voice_command(command)
                    time.sleep(0.5)
                except Exception as e:
                    time.sleep(1)
        
        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()

    def listen(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=4)
            command = self.recognizer.recognize_google(audio, language="ru-RU").lower()
            self.log_message(f"🎤 Вы: {command}")
            return command
        except:
            return ""

    def process_voice_command(self, command):
        command_lower = command.lower()
        
        # Активация по имени
        if "питер" in command_lower or "петр" in command_lower:
            if "привет" in command_lower:
                self.speak("Привет! Рада вас слышать! Чем могу помочь?")
            elif "спасибо" in command_lower:
                self.speak("Всегда пожалуйста! Обращайтесь ещё!")
            elif "пока" in command_lower:
                self.speak("До свидания! Буду ждать наших встреч!")
                self.on_close()
        
        # Время и дата
        elif any(word in command_lower for word in ["время", "который час", "сколько времени"]):
            self.speak_time_date()
        
        # Команды приложений
        elif "ютуб" in command_lower or "youtube" in command_lower:
            if "закрой" in command_lower:
                self.speak("Закрываю YouTube!")
                pyautogui.hotkey('ctrl', 'w')
            else:
                self.speak("Сделано! Открываю YouTube")
                self.open_youtube()
        
        elif "дискорд" in command_lower:
            self.speak("Готово! Запускаю Discord")
            self.launch_discord()
        
        elif "стим" in command_lower:
            self.speak("Сделано! Запускаю Steam")
            self.launch_steam()
        
        elif "скинченджер" in command_lower or "skinchanger" in command_lower:
            self.speak("Готово! Запускаю SkinChanger")
            self.launch_skinchanger()
        
        elif "браузер" in command_lower:
            self.speak("Сделано! Открываю браузер")
            self.launch_browser()
        
        # Системные команды
        elif "выключи компьютер" in command_lower:
            self.speak("Выключаю компьютер!")
            self.shutdown_pc()
        
        elif "перезагрузи" in command_lower:
            self.speak("Перезагружаю компьютер!")
            self.restart_pc()
        
        elif "скриншот" in command_lower:
            self.speak("Сделано! Делаю скриншот")
            self.take_screenshot()
        
        else:
            self.speak("Не поняла команду. Попробуйте ещё раз")

    def on_close(self):
        self.is_listening = False
        self.speak("До свидания! Возвращайтесь скорее!")
        self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PeterElegantAssistant()
    app.run()