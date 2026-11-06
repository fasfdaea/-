#!/usr/bin/env python3
"""Настройка Colorama и краткая интроспекция её публичного API."""

import inspect

import colorama
from colorama import Back, Cursor, Fore, Style


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


def main():
    print("Если Colorama ещё не установлена, выполните команду:")
    print("python3 -m pip install colorama")
    print("Эта команда установит библиотеку для цветного текста в терминале.\n")

    # None оставляет автоматический выбор convert/strip на усмотрение Colorama.
    colorama.init(autoreset=True, convert=None, strip=None, wrap=True)
    try:
        print(f"Colorama {colorama.__version__}")
        print(Fore.GREEN + "Зелёный текст" + Style.RESET_ALL)
        print(Back.YELLOW + Fore.BLACK + "Текст на цветном фоне")
        print(Style.BRIGHT + "Яркий текст")

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