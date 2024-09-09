import datetime
import os
from tqdm import tqdm
from Filters import Filters
import Options as options

class DiskUsageCalculator:
    def __init__(self, directory):
        self.max_name_length = 0
        self.directory = directory
        self.size_unit_choice = ""
        self.filters = Filters(directory)
        self.total_size = 0
        self.total_file_count = 0
        self.file_count = 0
        self.file_size = 0

    def get_file_size(self, path):
        try:
            if os.path.isfile(path):
                size = os.path.getsize(path)
                return size if size is not None else 0
            if os.path.isdir(path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        size = os.path.getsize(file_path)
                        if size is not None:
                            total_size += size
                return total_size
        except (OSError, PermissionError):
                pass

    def get_files_in_directory(self, max_depth=None):
        files = []
        for root, file, filenames in os.walk(self.directory):
            if max_depth is not None:
                current_depth = root[len(self.directory):].count(os.path.sep)
                if current_depth > max_depth:
                    continue
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if os.path.exists(file_path):
                    files.append(file_path)
        return files

    def apply_filter(self, file, filter, max_depth):
        try:
            size = self.get_file_size(file)
            file_extension = os.path.splitext(file)[-1].lower()
            file_creation_time = os.path.getmtime(file)
            creation_date = datetime.date.fromtimestamp(file_creation_time).strftime("%d-%m-%Y")

            if (filter['extension_filter'] is None or filter['extension_filter'] == file_extension) and \
               (filter['date_filter'] is None or filter['date_filter'] == creation_date) and \
                    (filter['depth_filter'] is None or filter['depth_filter'] == max_depth):
                filter['file_count'] += 1
                filter['file_size'] += size
        except OSError:
            pass

    def convert_size(self, size, unit):
        units = {
            'bytes': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3
        }
        if size is not None:
            converted_size = size / units[unit]
            if converted_size.is_integer():
                return f"{int(converted_size)} {unit}"
            else:
                return f"{converted_size:.4f} {unit}"
        else:
            return "N/A"

    def print_filter_results(self, filter, max_depth):
        extension_filter = filter['extension_filter']
        date_filter = filter['date_filter']

        description_parts = []

        if extension_filter:
            description_parts.append(f"{extension_filter} файлов")
        else:
            description_parts.append("файлов")

        if date_filter:
            description_parts.append(f", созданных {date_filter}")

        if max_depth is not None:
            description_parts.append(f" с {max_depth} уровнем вложенности")

        if description_parts[0] == "файлов":
            description_parts.append(" без фильтров")

        description = "".join(description_parts)
        file_size_formatted = self.convert_size(filter['file_size'], self.size_unit_choice)
        print(f"Общий объём {description}: {file_size_formatted}")
        print(f"Количество {description}: {filter['file_count']}")
        print()

    def visualize_directory_tree(self, path, indent=""):
        entries_info = []

        def collect_entries_info(path, indent, is_last=False):
            try:
                file_size = self.get_file_size(path)
                formatted_size = self.convert_size(file_size, self.size_unit_choice)
                name = f"{indent}{'└' if is_last else '├'} {os.path.basename(path)}{'/' if os.path.isdir(path) else ''}"
                entries_info.append((name, formatted_size, file_size))
                if os.path.isdir(path):
                    with os.scandir(path) as directory:
                        entries = list(directory)
                        entries.sort(key=lambda entry: (not entry.is_dir(), entry.name))
                        for i, entry in enumerate(entries):
                            new_indent = f"{indent}{'│ ' if not is_last else ' '}"
                            is_last_entry = i == len(entries) - 1
                            collect_entries_info(entry.path, new_indent, is_last=is_last_entry)
            except PermissionError:
                pass

        collect_entries_info(path, indent, is_last=True)

        max_name_length = max(len(name) for name, _, _ in entries_info)

        for name, formatted_size, file_size in entries_info:
            if file_size is not None and name[-1] != '/'\
                    and file_size > self.total_size * 0.1\
                    and file_size != self.total_size:
                print(f"\033[36m{name.ljust(max_name_length)} {formatted_size}")
            else:
                print(f"\033[0m{name.ljust(max_name_length)} {formatted_size}")

    def calculate_total_size(self, all_files):
        self.total_size = sum(
            self.get_file_size(file) if self.get_file_size(file) is not None else 0 for file in all_files)
        self.total_file_count += len(all_files)

    def print_total_summary(self):
        while True:
            self.size_unit_choice = input("\nВыберите единицы измерения для вывода объёма файлов (bytes/KB/MB/GB): ")
            if self.size_unit_choice not in options.get_units_options():
                print("ОШИБКА: Некорректные единицы измерения, повторите попытку.")
            else:
                break
        total_size_formatted = self.convert_size(self.total_size, self.size_unit_choice)
        print(f"Общий объём всех файлов: {total_size_formatted}")
        print(f"Количество всех файлов: {self.total_file_count}\n")

    def ask_visualize_directory_tree(self):
        while True:
            choice = input("Хотите ли вывести визуализацию дерева папок? (yes/no): ").lower()
            if choice in options.get_yes_options():
                self.visualize_directory_tree(self.directory)
                break
            elif choice in options.get_no_options():
                break
            else:
                print("Повторите попытку")

        input("\033[0mДля выхода из программы нажмите Enter ")

    def calculate_disk_usage(self, extension_filter=None, date_filter_=None, max_depth=None):
        all_files = self.get_files_in_directory(None)
        files = self.get_files_in_directory(max_depth) if max_depth is not None else all_files

        self.filters.add_filter(extension_filter, date_filter_, max_depth)

        for file in tqdm(files, position=0, desc="Анализ файлов", colour='white'):
            for filter in self.filters.filters:
                self.apply_filter(file, filter, max_depth)

        self.calculate_total_size(all_files)
        self.print_total_summary()

        for filter in self.filters.filters:
            self.print_filter_results(filter, max_depth)

        self.ask_visualize_directory_tree()