import os
from PIL import Image
import pillow_avif
from tqdm import tqdm

def convert_avif_to_format(input_path, output_path, format_choice):
    # Открываем AVIF изображение
    with Image.open(input_path) as img:
        # Определяем формат сохранения
        if format_choice == 1:
            output_path = output_path + ".jpg"
            img.save(output_path, "JPEG", lossless=True, quality=100)
            print(f"Файл сохранен в формате JPG: {output_path}")
        elif format_choice == 2:
            output_path = output_path + ".png"
            img.save(output_path, "PNG", lossless=True, quality=100)
            print(f"Файл сохранен в формате PNG: {output_path}")
        else:
            print("Недопустимый выбор формата.")

def process_images_in_folder(folder_path, format_choice):
    # Получаем список файлов в папке
    files = os.listdir(folder_path)

    # Отфильтровываем только AVIF файлы
    avif_files = [file for file in files if file.lower().endswith(".avif")]

    # Проверяем, что есть AVIF файлы
    if not avif_files:
        print("Нет файлов формата AVIF в папке.")
        return

    # Создаем прогресс-бар
    progress_bar = tqdm(avif_files, ncols=80, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")

    # Перебираем файлы
    for file in progress_bar:
        # Получаем путь к исходному файлу и путь к папке вывода
        input_path = os.path.join(folder_path, file)
        output_folder_path = os.path.dirname(input_path)

        # Получаем имя файла без расширения
        file_name = os.path.splitext(file)[0]

        # Вызываем функцию конвертации с выбранным форматом
        convert_avif_to_format(input_path, os.path.join(output_folder_path, file_name), format_choice)

# Получаем путь к текущей папке скрипта
current_folder = os.path.dirname(os.path.abspath(__file__))

# Выводим меню выбора формата
print("Выберите формат сохранения для всех файлов:")
print("1. JPG")
print("2. PNG")
format_choice = int(input("Введите число: "))

# Обрабатываем изображения в текущей папке
process_images_in_folder(current_folder, format_choice)

input("Нажмите Enter для выхода...")