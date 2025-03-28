import os
import shutil
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара

def is_directory_empty(directory):
    """Проверяет, пустая ли директория."""
    return not bool(os.listdir(directory))

def remove_empty_folders(together_dir):
    # Проходим по всем папкам в together
    for root, dirs, files in tqdm(os.walk(together_dir, topdown=False), desc="Обработка папок"):
        # Проверяем, есть ли папки images и labels в текущей директории
        if 'images' in dirs and 'labels' in dirs:
            images_dir = os.path.join(root, 'images')

            # Проверяем, пустые ли обе папки
            if is_directory_empty(images_dir):
                # Удаляем родительскую папку
                shutil.rmtree(root)
                print(f"Удалена пустая папка: {root}")

if __name__ == "__main__":
    remove_empty_folders(
        together_dir='together'
    )