import os
import shutil


def split_basename(basename):
    # Пытаемся разделить по последнему подчеркиванию
    if '_' in basename:
        parts = basename.rsplit('_', 1)
        name_part, num_part = parts[0], parts[1]
        if num_part.isdigit():
            return (name_part, num_part)
    
    # Пытаемся найти числовой суффикс
    split_idx = None
    for i in range(len(basename)-1, -1, -1):
        if not basename[i].isdigit():
            split_idx = i + 1
            break
    
    if split_idx is None or split_idx == 0:
        return (None, None)
    
    num_part = basename[split_idx:]
    if not num_part.isdigit():
        return (None, None)
    
    name_part = basename[:split_idx]
    return (name_part, num_part)

def process_data(train_images_dir, train_labels_dir, output_dir):
    for img_name in os.listdir(train_images_dir):
        # Пропускаем не-изображения
        if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            continue
            
        base, ext = os.path.splitext(img_name)
        folder, number = split_basename(base)
        
        # Определяем пути назначения
        if folder and number:
            img_dest_dir = os.path.join(output_dir, folder, 'images')
            label_dest_dir = os.path.join(output_dir, folder, 'labels')
            new_img_name = f"{number}{ext}"
            new_label_name = f"{number}.txt"
        else:
            img_dest_dir = os.path.join(output_dir, 'mixed', 'images')
            label_dest_dir = os.path.join(output_dir, 'mixed', 'labels')
            new_img_name = img_name
            new_label_name = f"{base}.txt"
        
        # Создаем директории
        os.makedirs(img_dest_dir, exist_ok=True)
        os.makedirs(label_dest_dir, exist_ok=True)
        
        # Копируем изображение
        src_img = os.path.join(train_images_dir, img_name)
        dst_img = os.path.join(img_dest_dir, new_img_name)
        shutil.copy2(src_img, dst_img)
        
        # Копируем метку если существует
        src_label = os.path.join(train_labels_dir, f"{base}.txt")
        if os.path.exists(src_label):
            dst_label = os.path.join(label_dest_dir, new_label_name)
            shutil.copy2(src_label, dst_label)

if __name__ == "__main__":
    process_data(
        train_images_dir='val/images',
        train_labels_dir='val/labels',
        output_dir='common'
    )