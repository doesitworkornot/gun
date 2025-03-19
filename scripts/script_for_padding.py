import cv2
import os
import argparse
import numpy as np

ALLOWED_SUBFOLDERS = [
    'div',
    'only_guns',
    'guns',
    'vids',
    'films',
    'mixed'
]


def add_padding_to_square(img):
    """Добавляет паддинг для получения квадратного изображения и возвращает паддинги"""
    padding_color = (114, 114, 114)
    h, w = img.shape[:2]
    if h == w:
        return img, (0, 0, 0, 0)

    if h > w:
        pad_left = (h - w) // 2
        pad_right = h - w - pad_left
        pad_top, pad_bottom = 0, 0
    else:
        pad_top = (w - h) // 2
        pad_bottom = w - h - pad_top
        pad_left, pad_right = 0, 0

    img_padded = cv2.copyMakeBorder(img, pad_top, pad_bottom, pad_left, pad_right,
                                    cv2.BORDER_CONSTANT, value=padding_color)
    return img_padded, (pad_top, pad_bottom, pad_left, pad_right)


def process_folder(input_img_dir, input_label_dir, output_img_dir, output_label_dir, new_size):
    new_width, new_height = new_size
    new_area = new_width * new_height

    processed_count = 0
    for filename in os.listdir(input_img_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            continue

        img_path = os.path.join(input_img_dir, filename)
        img = cv2.imread(img_path)
        if img is None:
            continue

        # Обработка bounding boxes
        root, _ = os.path.splitext(filename)
        bbox_filename = f"{root}.txt"
        bbox_path = os.path.join(input_label_dir, bbox_filename)
        lines = []
        min_area = None
        best_class_id = None
        zero_class = False
        first_class = False

        if os.path.exists(bbox_path):
            with open(bbox_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 5:
                    continue
                class_id, x_center, y_center, bbox_width, bbox_height = map(float, parts)
                if class_id == 0:
                    zero_class = True
                else:
                    first_class = True
        # Расчет масштаба
        scale = 1.0
        if zero_class and not first_class:
            scale = 4
        elif not zero_class and first_class:
            scale = 2
        elif zero_class and first_class:
            sclale = 3

        # Добавление паддингов
        img_padded, (pad_top, pad_bottom, pad_left, pad_right) = add_padding_to_square(img)
        h_padded, w_padded = img_padded.shape[:2]

        # Конволюционный паддинг
        conv_padding = int((scale - 1) * h_padded // 2)
        total_padding = conv_padding * 2

        if conv_padding > 0:
            img_final = cv2.copyMakeBorder(img_padded, conv_padding, conv_padding, conv_padding, conv_padding,
                                           cv2.BORDER_CONSTANT, value=(114, 114, 114))
        else:
            img_final = img_padded

        # Ресайз и сохранение
        resized_img = cv2.resize(img_final, new_size, interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(output_img_dir, filename), resized_img)

        # Обновление bounding boxes
        if lines:
            new_lines = []
            padded_w = w_padded + total_padding
            padded_h = h_padded + total_padding

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 5:
                    continue
                class_id, x_center, y_center, bbox_width, bbox_height = map(float, parts)

                # Коррекция координат
                x_abs = x_center * img.shape[1] + pad_left
                y_abs = y_center * img.shape[0] + pad_top
                new_x = (x_abs + conv_padding) / padded_w
                new_y = (y_abs + conv_padding) / padded_h
                new_w = (bbox_width * img.shape[1]) / padded_w
                new_h = (bbox_height * img.shape[0]) / padded_h

                new_lines.append(f"{int(class_id)} {new_x:.6f} {new_y:.6f} {new_w:.6f} {new_h:.6f}\n")

            # Сохранение новых bounding boxes
            output_bbox_path = os.path.join(output_label_dir, bbox_filename)
            with open(output_bbox_path, 'w') as f:
                f.writelines(new_lines)

        processed_count += 1
        if processed_count % 100 == 0:
            print(f"Обработано {processed_count} изображений в {input_img_dir}")


def process_all_folders(base_input, base_output, new_size):
    for subfolder in ALLOWED_SUBFOLDERS:
        # Формирование путей
        input_img_dir = os.path.join(base_input, subfolder, 'images')
        input_label_dir = os.path.join(base_input, subfolder, 'labels')
        output_img_dir = os.path.join(base_output, subfolder, 'images')
        output_label_dir = os.path.join(base_output, subfolder, 'labels')

        if not os.path.exists(input_img_dir):
            print(f"Пропускаем несуществующую папку: {input_img_dir}")
            continue

        print(f"\nОбработка папки: {input_img_dir}")
        os.makedirs(output_img_dir, exist_ok=True)
        os.makedirs(output_label_dir, exist_ok=True)

        process_folder(
            input_img_dir,
            input_label_dir,
            output_img_dir,
            output_label_dir,
            new_size
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка изображений для детекции объектов")
    parser.add_argument("input_folder", help="Корневая папка с изображениями и разметкой")
    parser.add_argument("output_folder", help="Выходная папка для изображений")
    args = parser.parse_args()

    process_all_folders(
        base_input=args.input_folder,
        base_output=args.output_folder,
        new_size=(640, 640)
    )
    print("Обработка всех указанных папок завершена!")