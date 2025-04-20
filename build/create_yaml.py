import os
import yaml

def read_validation_folders(validation_file):
    """Читает файл to_val.txt и возвращает список папок для валидации."""
    with open(validation_file, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def create_yolo_yaml(dataset_dir, validation_file, output_yaml):
    # Читаем список папок для валидации
    validation_folders = read_validation_folders(validation_file)

    # Собираем пути для train и val
    train_paths = []
    val_paths = []

    # Проходим по всем папкам в dataset
    for folder_name in os.listdir(dataset_dir):
        folder_path = os.path.join(dataset_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Определяем, куда добавить папку (val или train)
        if folder_name in validation_folders:
            val_paths.append(os.path.join(folder_name, "images", "val"))
        else:
            train_paths.append(os.path.join(folder_name, "images", "train"))

    # Создаем структуру YAML
    yaml_data = {
        "path": dataset_dir,  # Основной путь до датасета
        "train": train_paths,  # Список путей для тренировки
        "val": val_paths,      # Список путей для валидации
        "names": {             # Пример классов (замените на свои)
            0: "gun",
            1: "pistol",
        }
    }

    # Сохраняем YAML в файл
    with open(output_yaml, 'w', encoding='utf-8') as file:
        yaml.dump(yaml_data, file, default_flow_style=False)

    print(f"YAML файл создан: {output_yaml}")

if __name__ == "__main__":
    create_yolo_yaml(
        dataset_dir='dataset',
        validation_file='to_val.txt',
        output_yaml='dataset_config.yaml'
    )