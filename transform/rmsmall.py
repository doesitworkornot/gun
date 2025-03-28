import os
import shutil
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара

def process_merged_folder(merged_dir, output_dir):
    # Создаем директории filtred и filtred/small
    filtred_dir = os.path.join(output_dir, "filtred")
    small_images_dir = os.path.join(output_dir, "filtred", "small", "images")
    small_labels_dir = os.path.join(output_dir, "filtred", "small", "labels")
    os.makedirs(filtred_dir, exist_ok=True)
    os.makedirs(small_images_dir, exist_ok=True)
    os.makedirs(small_labels_dir, exist_ok=True)

    # Проходим по всем папкам в merged
    for folder_name in tqdm(os.listdir(merged_dir), desc="Обработка папок"):
        folder_path = os.path.join(merged_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Проверяем папку images
        images_dir = os.path.join(folder_path, "images")
        labels_dir = os.path.join(folder_path, "labels")
        if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
            continue

        # Считаем количество изображений
        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        num_images = len(image_files)

        # Обрабатываем в зависимости от количества изображений
        if num_images < 10:
            # Если изображений меньше 10, копируем содержимое в small
            for image_file in tqdm(image_files, desc=f"Копирование {folder_name} в small"):
                base_name, ext = os.path.splitext(image_file)
                label_file = os.path.join(labels_dir, f"{base_name}.txt")

                # Копируем изображение
                new_image_name = f"{folder_name}_{image_file}"
                shutil.copy2(os.path.join(images_dir, image_file), os.path.join(small_images_dir, new_image_name))

                # Копируем соответствующий .txt файл, если он существует
                if os.path.exists(label_file):
                    new_label_name = f"{folder_name}_{base_name}.txt"
                    shutil.copy2(label_file, os.path.join(small_labels_dir, new_label_name))
        else:
            # Если изображений 10 или больше, копируем всю папку в filtred
            dest_folder = os.path.join(filtred_dir, folder_name)
            shutil.copytree(folder_path, dest_folder)

if __name__ == "__main__":
    process_merged_folder(
        merged_dir='merge',
        output_dir='output'
    )