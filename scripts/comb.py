import os
import shutil
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара

def process_fold_folder(fold_dir, output_dir):
    # Создаем директории для images и labels в together
    together_images_dir = os.path.join(output_dir, "together", "images")
    together_labels_dir = os.path.join(output_dir, "together", "labels")
    os.makedirs(together_images_dir, exist_ok=True)
    os.makedirs(together_labels_dir, exist_ok=True)

    # Проходим по всем папкам в fold
    for folder_name in tqdm(os.listdir(fold_dir), desc="Обработка папок"):
        folder_path = os.path.join(fold_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Проверяем наличие папок images и labels
        images_dir = os.path.join(folder_path, "images")
        labels_dir = os.path.join(folder_path, "labels")
        if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
            continue

        # Копируем файлы из images
        for image_file in tqdm(os.listdir(images_dir), desc=f"Копирование изображений из {folder_name}"):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                base_name, ext = os.path.splitext(image_file)
                new_image_name = f"{folder_name}_{image_file}"
                shutil.copy2(
                    os.path.join(images_dir, image_file),
                    os.path.join(together_images_dir, new_image_name)
                )

        # Копируем файлы из labels
        for label_file in tqdm(os.listdir(labels_dir), desc=f"Копирование меток из {folder_name}"):
            if label_file.lower().endswith('.txt'):
                base_name, ext = os.path.splitext(label_file)
                new_label_name = f"{folder_name}_{label_file}"
                shutil.copy2(
                    os.path.join(labels_dir, label_file),
                    os.path.join(together_labels_dir, new_label_name)
                )

if __name__ == "__main__":
    process_fold_folder(
        fold_dir='films',
        output_dir='film'
    )