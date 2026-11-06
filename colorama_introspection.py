#!/usr/bin/env python3
"""Настройка Colorama и краткая интроспекция её публичного API."""

import inspect
import os
import shlex
import sys
from pathlib import Path


def python_command(*arguments):
    """Создаёт команду запуска для текущей системы и Python."""
    executable = sys.executable
    if os.name == "nt" and executable.lower().endswith("pythonw.exe"):
        executable = executable[:-len("pythonw.exe")] + "python.exe"
    parts = [executable, *(str(argument) for argument in arguments)]
    if os.name == "nt":
        quoted_parts = ["'" + part.replace("'", "''") + "'" for part in parts]
        return "& " + " ".join(quoted_parts)
    return shlex.join(parts)

try:
    import colorama
    from colorama import Back, Cursor, Fore, Style
except ModuleNotFoundError as error:
    if error.name != "colorama":
        raise
    print("Не найдена библиотека Colorama.")
    print("Чтобы скачать и установить Colorama, скопируй команду в PowerShell или системный терминал:")
    print(python_command("-m", "pip", "install", "colorama"))
    print("Нажми Enter и дождись окончания установки.")
    print("Не вводи её в окно Python Shell. После установки снова запусти этот файл из своей программы.")
    raise SystemExit(1)


def show_color_constants(name, group):
    """Показывает строковые ANSI-константы или методы выбранной группы."""
    print(f"\n{name}:")
    members = inspect.getmembers(group)
    constants = [(attribute, value) for attribute, value in members
                 if not attribute.startswith("_") and isinstance(value, str)]
    methods = [(attribute, value) for attribute, value in members
               if not attribute.startswith("_") and callable(value)]

    for attribute, value in constants:
        print(f"  {attribute:<12} = {value!r}")
    for attribute, method in methods:
        print(f"  {attribute}{inspect.signature(method)}")


def show_function_signatures():
    """Выводит сигнатуры наиболее важных функций Colorama."""
    print("\nОсновные функции:")
    for name in ("init", "just_fix_windows_console", "deinit", "reinit"):
        function = getattr(colorama, name)
        print(f"  {name}{inspect.signature(function)}")


def practice():
    """Просит пользователя повторить пример со своим текстом."""
    print("\nПрактика: попробуйте вывести свой текст зелёным цветом.")
    print("Когда появится приглашение ниже, введите: Hello my neighbour")
    print("Введите только эти слова: без Fore.GREEN, кавычек и точки.")
    text = input("Ваш текст: ")
    print("Ваш результат:")
    print(Fore.GREEN + text + Style.RESET_ALL)
    print("\nЧтобы получить такой же результат в своей программе, создай файл hello.py и вставь туда:")
    print("from colorama import Fore, init")
    print("init(autoreset=True)")
    print(f"print(Fore.GREEN + {text!r})")
    print("\nСохрани этот код в новом файле hello.py.")
    print("VS Code: нажми Ctrl+S, затем кнопку Run Python File (треугольник).")
    print("IDLE: нажми F5 или выбери Run -> Run Module.")


def main():
    # None оставляет автоматический выбор convert/strip на усмотрение Colorama.
    colorama.init(autoreset=True, convert=None, strip=None, wrap=True)
    try:
        print(f"Colorama {colorama.__version__}")
        print(Fore.GREEN + "Зелёный текст" + Style.RESET_ALL)
        print(Back.YELLOW + Fore.BLACK + "Текст на цветном фоне")
        print(Style.BRIGHT + "Яркий текст")

        practice()

        show_color_constants("Fore: цвет текста", Fore)
        show_color_constants("Back: цвет фона", Back)
        show_color_constants("Style: стиль текста", Style)
        show_color_constants("Cursor: управление курсором", Cursor)
        show_function_signatures()
    finally:
        # Возвращаем стандартные потоки в исходное состояние.
        colorama.deinit()


if __name__ == "__main__":
    main()