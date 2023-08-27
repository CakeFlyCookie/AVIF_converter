#pip install pillow=9.5.0 pillow-avif-plugin tqdm
#хуево работает, меняет палитру изображений/делает контрастными, хуй знает как пофиксить, смена на adobe/apple icc тоже не помогла
import os
from PIL import Image
from tqdm import tqdm
import pillow_avif

# Путь к папке с изображениями (рядом со скриптом)
script_folder = os.path.dirname(os.path.abspath(__file__))
image_folder = script_folder

# Получаем список изображений в папке
image_files = [
    os.path.join(image_folder, filename)
    for filename in os.listdir(image_folder)
    if os.path.isfile(os.path.join(image_folder, filename))
    and not filename.lower().endswith(".avif")
]

# Инициализация прогресс-бара
progress_bar = tqdm(total=len(image_files), desc="Сжатие изображений", unit="изображение",
                    bar_format="{desc}: {percentage:.0f}%|{bar}| {n_fmt}/{total_fmt}",
                    ncols=80, colour='green')

# Проходим по каждому изображению
for image_file in image_files:
    try:
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