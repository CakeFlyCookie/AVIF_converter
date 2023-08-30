#version 8 / encoder_v3
#pip install pillow=9.5.0 pillow-avif-plugin tqdm
#хуево работает, меняет палитру изображений/делает контрастными, хуй знает как пофиксить, смена на adobe/apple icc тоже не помогла
#работает не только с файлами из папки но и из подпапок

import os
from PIL import Image
from tqdm import tqdm
import pillow_avif

# Путь к папке с изображениями (рядом со скриптом)
script_folder = os.path.dirname(os.path.abspath(__file__))
image_folder = script_folder

# Получаем список всех файлов из папки и её подпапок
image_files = []
for root, _, filenames in os.walk(image_folder):
    for filename in filenames:
        if not filename.lower().endswith(".avif"):
            image_files.append(os.path.join(root, filename))

# Инициализация прогресс-бара
progress_bar = tqdm(total=len(image_files), desc="Сжатие изображений", unit="изображение",
                    bar_format="{desc}: {percentage:.0f}%|{bar}| {n_fmt}/{total_fmt}",
                    ncols=80, colour='green')

# Проходим по каждому изображению
for image_file in image_files:
    try:
        # Проверяем, если файл имеет расширение .gif, пропускаем его
        if image_file.lower().endswith(".gif"):
            continue

        # Открываем изображение с помощью Pillow
        image = Image.open(image_file)

        # Создаем новое имя файла с расширением .avif
        new_file = os.path.splitext(image_file)[0] + ".avif"

        # Сохраняем изображение в формате AVIF с палитрой цветов и без потерь
        image.save(new_file, "AVIF", save_all=True, lossless=True, subsampling="4:4:4")

        # Обновляем прогресс-бар
        progress_bar.update(1)
        progress_bar.set_postfix(files_done=progress_bar.n)

       # tqdm.write(f"Изображение '{image_file}' сжато без потерь в формат AVIF: '{new_file}'")
    except Exception as e:
        tqdm.write(f"Ошибка при обработке файла '{image_file}': {str(e)}")

# Завершаем прогресс-бар
progress_bar.close()

input("Нажмите Enter для выхода...")
