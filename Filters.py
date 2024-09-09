import datetime
import os
import sys

import Options as options
from HelpMessage import display_help_message

class Filters:
    def __init__(self, directory):
        self.directory = directory
        self.filters = []

    @staticmethod
    def get_directory_input():
        while True:
            directory = input("Введите путь к каталогу: ")
            if os.path.exists(directory):
                print("Если вы хотите узнать, что умеет программа, напишите help, -h, --help: ")
                return directory
            elif directory.lower() in options.get_help_options():
                display_help_message()
            elif directory.lower() in options.get_exit_options():
                input("Программа была завершена досрочно. Для выхода нажмите Enter ")
                sys.exit()
            else:
                print("ОШИБКА: Путь к каталогу не существует, повторите попытку.")

    @staticmethod
    def get_extension_filter_input():
        while True:
            extension_filter = input(
                "Введите расширение файлов для фильтрации (или оставьте пустым для всех расширений): ").lower()
            if not extension_filter:
                return None
            elif extension_filter.startswith(".") and extension_filter[1:].isascii():
                return extension_filter
            elif extension_filter.lower() in options.get_help_options():
                display_help_message()
            elif extension_filter.lower() in options.get_exit_options():
                print("Программа была завершена досрочно.")
                sys.exit()
            else:
                print("ОШИБКА: Расширение должно начинаться с точки (например, '.txt')"
                      " и существовать, повторите попытку.")

    @staticmethod
    def get_date_filter_input():
        while True:
            date_filter_str = input("Введите дату создания файлов (в формате ДД-ММ-ГГГГ) "
                                    "для фильтрации (или оставьте пустым для всех дат): ")
            if date_filter_str.lower() in options.get_help_options():
                display_help_message()
            elif date_filter_str.lower() in options.get_exit_options():
                print("Программа была завершена досрочно.")
                sys.exit()
            elif date_filter_str:
                try:
                    date_filter = datetime.datetime.strptime(date_filter_str, "%d-%m-%Y").date()
                    return date_filter
                except ValueError:
                    print("ОШИБКА: Неверный формат даты, повторите попытку.")
            else:
                return None

    @staticmethod
    def get_max_depth_input():
        while True:
            max_depth_str = input("Введите максимальный уровень вложенности (оставьте пустым для без ограничений): ")
            if max_depth_str.lower() in options.get_help_options():
                display_help_message()
            elif max_depth_str.lower() in options.get_exit_options():
                print("Программа была завершена досрочно.")
                sys.exit()
            elif max_depth_str:
                try:
                    max_depth = int(max_depth_str)
                    if max_depth < 0:
                        raise ValueError("ОШИБКА: уровень вложенности должен"
                                         " быть больше или равен нулю, повторите попытку")
                    return max_depth
                except ValueError:
                    print("ОШИБКА: уровень вложенности должен быть больше или равен нулю, повторите попытку.")
            else:
                return None


    def add_filter(self, extension_filter=None, date_filter=None, max_depth=None):
        self.filters.append({
            'extension_filter': extension_filter.lower() if extension_filter else None,
            'date_filter': date_filter.strftime("%d-%m-%Y") if date_filter else None,
            'depth_filter': max_depth if max_depth else None,
            'file_count': 0,
            'file_size': 0
        })