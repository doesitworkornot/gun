import os
import shutil
import yaml
from PIL import Image

# Загрузка конфигурации из YAML-файла
def load_yaml_config(yaml_path):
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Загрузка конфигурации
yaml_path = '/home/jovyan/work/yolo_train/sort.yaml'  # Укажите путь к вашему YAML-файлу
config = load_yaml_config(yaml_path)

# Получение базового пути и путей для обучения
base_path = config['path']
train_image_paths = [os.path.join(base_path, path) for path in config['train_images']]
train_ann_paths = [os.path.join(base_path, path) for path in config['train_annotations']]

# Функция letterbox для ресайза изображения с сохранением пропорций
def letterbox(image, target_size=(640, 640)):
    width, height = image.size
    scale = min(target_size[0] / width, target_size[1] / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = image.resize((new_width, new_height), Image.BILINEAR)
    new_image = Image.new("RGB", target_size, (0, 0, 0))
    new_image.paste(resized_image, ((target_size[0] - new_width) // 2, (target_size[1] - new_height) // 2))
    return new_image

# Функция для вычисления площади bounding box
def calculate_area(x_center, y_center, width, height, img_width, img_height):
    abs_width = width * img_width
    abs_height = height * img_height
    return abs_width * abs_height

# Пути к новой папке only_guns
only_guns_dir = 'only_guns'
images_train_dir = os.path.join(only_guns_dir, 'images', 'train')
labels_dir = os.path.join(only_guns_dir, 'labels')

# Создание новых папок
os.makedirs(images_train_dir, exist_ok=True)
os.makedirs(labels_dir, exist_ok=True)

# Обработка всех путей для обучения
for images_source_dir, labels_source_dir in zip(train_image_paths, train_ann_paths):
    # Получение списка всех изображений и меток
    images = sorted(os.listdir(images_source_dir))
    labels = sorted(os.listdir(labels_source_dir))

    # Убедимся, что количество изображений и меток совпадает
    if len(images) != len(labels):
        print(f"Предупреждение: количество изображений и меток не совпадает в {images_source_dir}")
        continue  # Пропускаем эту папку, если количество файлов не совпадает

    # Проходим по всем изображениям и меткам
    for img_name, lbl_name in zip(images, labels):
        # Полные пути к файлам
        img_path = os.path.join(images_source_dir, img_name)
        lbl_path = os.path.join(labels_source_dir, lbl_name)

        # Пытаемся открыть изображение
        try:
            image = Image.open(img_path)
            img_width, img_height = image.size
        except Exception as e:
            print(f"Ошибка при открытии изображения {img_path}: {e}")
            continue  # Пропускаем это изображение

        # Пытаемся открыть файл с метками
        try:
            with open(lbl_path, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Ошибка при открытии файла меток {lbl_path}: {e}")
            continue  # Пропускаем этот файл меток

        # Проверяем, есть ли bounding box с площадью больше 30000
        has_large_box = False
        for line in lines:
            # Убираем пробелы и проверяем, что строка не пустая
            line = line.strip()
            if not line:
                continue  # Пропускаем пустые строки

            # Парсим метку (class_id, x_center, y_center, width, height)
            try:
                class_id, x_center, y_center, width, height = map(float, line.split())
            except ValueError as e:
                print(f"Ошибка при разборе строки в файле {lbl_name}: {line}. Ошибка: {e}")
                continue  # Пропускаем некорректные строки

            # Вычисляем площадь bounding box
            area = calculate_area(x_center, y_center, width, height, img_width, img_height)
            if area > 30000:
                has_large_box = True
                break

        # Если найден bounding box с площадью больше 30000
        if has_large_box:
            # Ресайзим изображение с помощью letterbox
            resized_image = letterbox(image)

            # Сохраняем исходное изображение в папку only_guns/images/train
            original_image_path = os.path.join(images_train_dir, img_name)
            try:
                image.save(original_image_path)
            except Exception as e:
                print(f"Ошибка при сохранении изображения {original_image_path}: {e}")
                continue  # Пропускаем это изображение

            # Сохраняем метки в папку only_guns/labels
            new_lbl_path = os.path.join(labels_dir, lbl_name)
            try:
                shutil.copy(lbl_path, new_lbl_path)
            except Exception as e:
                print(f"Ошибка при копировании меток {lbl_path}: {e}")
                continue  # Пропускаем этот файл меток

            # Сохраняем ресайзнутое изображение (опционально, если нужно)
            resized_image_path = os.path.join(images_train_dir, f"resized_{img_name}")
            try:
                resized_image.save(resized_image_path)
            except Exception as e:
                print(f"Ошибка при сохранении ресайзнутого изображения {resized_image_path}: {e}")

print("Обработка завершена!")

images_dir = 'only_guns/images/train'  # Папка с изображениями
labels_dir = 'only_guns/labels'        # Папка с метками

# Функция для удаления файлов, начинающихся с "resized_"
def remove_resized_files(directory):
    # Получаем список всех файлов в папке
    files = os.listdir(directory)
    
    # Проходим по каждому файлу
    for file_name in files:
        # Если файл начинается с "resized_", удаляем его
        if file_name.startswith("resized_"):
            file_path = os.path.join(directory, file_name)
            try:
                os.remove(file_path)
                print(f"Удален файл: {file_path}")
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")

# Очищаем папку с изображениями
print("Очистка папки с изображениями...")
remove_resized_files(images_dir)

# Очищаем папку с метками
print("Очистка папки с метками...")
remove_resized_files(labels_dir)

print("Очистка завершена!")