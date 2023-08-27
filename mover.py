#v2 версия mover'a, работает + логи.
import os
import shutil
from collections import defaultdict
import logging

# 1. Определяем текущую рабочую директорию, где находится скрипт.
current_directory = os.path.dirname(os.path.abspath(__file__))

# 2. Собираем информацию о файлах во всех папках и подпапках текущей директории.
file_info = defaultdict(list)

for root, dirs, files in os.walk(current_directory):
    for file in files:
        filename, file_extension = os.path.splitext(file)
        file_info[root].append((filename, file_extension))

# 3. Создаем папку 'dubsmover' в текущей директории, если она не существует.
dubsmover_directory = os.path.join(current_directory, 'avifmover')
if not os.path.exists(dubsmover_directory):
    os.makedirs(dubsmover_directory)

# 4. Инициализируем логгер и настраиваем его для записи в файл log.log.
log_filename = os.path.join(current_directory, 'avifmover.log')
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 5. Идентифицируем файлы с одинаковыми именами и перемещаем их, с логированием.
for folder, files in file_info.items():
    filenames = set()
    for filename, file_extension in files:
        if filename in filenames and file_extension != '.avif':
            source_path = os.path.join(folder, f"{filename}{file_extension}")
            relative_path = os.path.relpath(source_path, current_directory)
            destination_path = os.path.join(dubsmover_directory, relative_path)
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.move(source_path, destination_path)
            # Логируем перемещение файла
            logging.info(f"Перемещен файл: {source_path} -> {destination_path}")
        else:
            filenames.add(filename)

# Логируем успешное завершение выполнения скрипта
logging.info("Скрипт успешно завершил выполнение")
