import os
import shutil
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара
import argparse

def read_validation_folders(validation_file):
    """Читает файл to_val.txt и возвращает список папок для валидации."""
    with open(validation_file, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def process_files_folder(files_dir, output_dir, validation_file):
    # Читаем список папок для валидации
    validation_folders = read_validation_folders(validation_file)

    # Проходим по всем папкам в files
    for folder_name in tqdm(os.listdir(files_dir), desc="Обработка папок"):
        folder_path = os.path.join(files_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Определяем, куда копировать (val или train)
        if folder_name in validation_folders:
            dest_type = "val"
        else:
            dest_type = "train"

        # Создаем целевые директории
        dest_images_dir = os.path.join(output_dir, folder_name, "images", dest_type)
        dest_labels_dir = os.path.join(output_dir, folder_name, "labels", dest_type)
        os.makedirs(dest_images_dir, exist_ok=True)
        os.makedirs(dest_labels_dir, exist_ok=True)

        # Копируем файлы из images
        images_dir = os.path.join(folder_path, "images")
        if os.path.exists(images_dir):
            for image_file in tqdm(os.listdir(images_dir), desc=f"Копирование изображений из {folder_name}"):
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    shutil.copy2(
                        os.path.join(images_dir, image_file),
                        os.path.join(dest_images_dir, image_file)
                    )

        # Копируем файлы из labels
        labels_dir = os.path.join(folder_path, "labels")
        if os.path.exists(labels_dir):
            for label_file in tqdm(os.listdir(labels_dir), desc=f"Копирование меток из {folder_name}"):
                if label_file.lower().endswith('.txt'):
                    shutil.copy2(
                        os.path.join(labels_dir, label_file),
                        os.path.join(dest_labels_dir, label_file)
                    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process files in a folder.')
    parser.add_argument('--files_dir', type=str, default='filtred', help='Directory with files to process')
    parser.add_argument('--output_dir', type=str, default='dataset', help='Output directory for processed files')
    parser.add_argument('--validation_file', type=str, default='files/to_val.txt', help='Path to validation file')

    args = parser.parse_args()

    process_files_folder(
        files_dir=args.files_dir,
        output_dir=args.output_dir,
        validation_file=args.validation_file
    )