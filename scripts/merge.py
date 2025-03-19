import os
import shutil
from collections import defaultdict
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара

def split_name(folder_name):
    """Разделяет имя папки по '_' или '-' и возвращает первую часть и оставшуюся часть."""
    for sep in ['_', '-']:
        if sep in folder_name:
            parts = folder_name.split(sep, 1)
            return parts[0], parts[1]
    return folder_name, None

def is_number_folder(folder_name):
    """Проверяет, состоит ли имя папки только из чисел."""
    return folder_name.isdigit()

def process_common_folder(common_dir, output_dir):
    # Словарь для группировки папок
    groups = defaultdict(list)

    # Проходим по всем папкам в common
    for folder_name in os.listdir(common_dir):
        folder_path = os.path.join(common_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Если папка состоит только из чисел, добавляем её в группу numbers
        if is_number_folder(folder_name):
            groups["numbers"].append(folder_name)
        else:
            # Иначе обрабатываем как раньше
            prefix, suffix = split_name(folder_name)
            groups[prefix].append((folder_name, suffix))

    # Обрабатываем каждую группу
    for prefix, folders in tqdm(groups.items(), desc="Обработка групп папок"):
        if prefix == "numbers":
            # Обрабатываем папки с числами
            dest_images = os.path.join(output_dir, "numbers", "images")
            dest_labels = os.path.join(output_dir, "numbers", "labels")
            os.makedirs(dest_images, exist_ok=True)
            os.makedirs(dest_labels, exist_ok=True)

            for folder_name in folders:
                src_images = os.path.join(common_dir, folder_name, "images")
                src_labels = os.path.join(common_dir, folder_name, "labels")

                # Копируем файлы только если .txt файл не пустой
                for file_name in tqdm(os.listdir(src_images), desc=f"Копирование {folder_name}"):
                    base_name, ext = os.path.splitext(file_name)
                    label_file = os.path.join(src_labels, f"{base_name}.txt")
                    
                    # Проверяем, существует ли файл и не пустой ли он
                    if os.path.exists(label_file) and os.path.getsize(label_file) > 0:
                        new_name = f"{folder_name}_{file_name}"
                        shutil.copy2(os.path.join(src_images, file_name), os.path.join(dest_images, new_name))
                        shutil.copy2(label_file, os.path.join(dest_labels, f"{folder_name}_{base_name}.txt"))
        else:
            # Обрабатываем остальные папки как раньше
            if len(folders) == 1:
                # Если группа состоит из одной папки, просто копируем
                folder_name, _ = folders[0]
                src_images = os.path.join(common_dir, folder_name, "images")
                src_labels = os.path.join(common_dir, folder_name, "labels")
                dest_images = os.path.join(output_dir, folder_name, "images")
                dest_labels = os.path.join(output_dir, folder_name, "labels")

                os.makedirs(dest_images, exist_ok=True)
                os.makedirs(dest_labels, exist_ok=True)

                # Копируем файлы только если .txt файл не пустой
                for file_name in tqdm(os.listdir(src_images), desc=f"Копирование {folder_name}"):
                    base_name, ext = os.path.splitext(file_name)
                    label_file = os.path.join(src_labels, f"{base_name}.txt")
                    
                    # Проверяем, существует ли файл и не пустой ли он
                    if os.path.exists(label_file) and os.path.getsize(label_file) > 0:
                        shutil.copy2(os.path.join(src_images, file_name), os.path.join(dest_images, file_name))
                        shutil.copy2(label_file, os.path.join(dest_labels, f"{base_name}.txt"))
            else:
                # Если группа состоит из нескольких папок, объединяем
                dest_images = os.path.join(output_dir, prefix, "images")
                dest_labels = os.path.join(output_dir, prefix, "labels")
                os.makedirs(dest_images, exist_ok=True)
                os.makedirs(dest_labels, exist_ok=True)

                for folder_name, suffix in folders:
                    src_images = os.path.join(common_dir, folder_name, "images")
                    src_labels = os.path.join(common_dir, folder_name, "labels")

                    # Копируем файлы только если .txt файл не пустой
                    for file_name in tqdm(os.listdir(src_images), desc=f"Копирование {folder_name}"):
                        base_name, ext = os.path.splitext(file_name)
                        label_file = os.path.join(src_labels, f"{base_name}.txt")
                        
                        # Проверяем, существует ли файл и не пустой ли он
                        if os.path.exists(label_file) and os.path.getsize(label_file) > 0:
                            new_name = f"{suffix}_{file_name}" if suffix else file_name
                            shutil.copy2(os.path.join(src_images, file_name), os.path.join(dest_images, new_name))
                            shutil.copy2(label_file, os.path.join(dest_labels, f"{suffix}_{base_name}.txt" if suffix else f"{base_name}.txt"))

if __name__ == "__main__":
    process_common_folder(
        common_dir='together',
        output_dir='merge'
    )