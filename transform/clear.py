import os
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара

def is_file_empty(file_path):
    """Проверяет, пустой ли файл (содержит ли только пробелы или пустые строки)."""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():  # Если строка не пустая (после удаления пробелов)
                return False
    return True

def remove_empty_labels_and_images(together_dir):
    # Проходим по всем папкам в together
    for root, dirs, _ in tqdm(os.walk(together_dir), desc="Обработка папок"):
        # Проверяем, есть ли папка labels в текущей директории
        if 'labels' in dirs:
            labels_dir = os.path.join(root, 'labels')
            images_dir = os.path.join(root, 'images')

            # Проходим по всем .txt файлам в папке labels
            for label_file in tqdm(os.listdir(labels_dir), desc="Проверка файлов"):
                if label_file.endswith('.txt'):
                    label_path = os.path.join(labels_dir, label_file)

                    # Проверяем, пустой ли файл (с учетом содержимого)
                    if is_file_empty(label_path):
                        # Удаляем пустой .txt файл
                        os.remove(label_path)
                        print(f"Удален пустой файл: {label_path}")

                        # Удаляем соответствующее изображение
                        image_name = os.path.splitext(label_file)[0] + '.jpg'
                        image_path = os.path.join(images_dir, image_name)
                        if os.path.exists(image_path):
                            os.remove(image_path)
                            print(f"Удалено изображение: {image_path}")

if __name__ == "__main__":
    remove_empty_labels_and_images(
        together_dir='together'
    )