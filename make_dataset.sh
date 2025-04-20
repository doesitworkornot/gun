#!/bin/bash

if [ -z "$1" ]; then
  echo "Ошибка: Не указан источник датасета."
  echo "Использование: $0 files_dir"
  exit 1
fi


if [ -d "dataset" ]; then
  echo "Очистка директории dataset..."
  rm -r dataset/*
else
  echo "Директория dataset не существует, создание..."
  mkdir -p dataset
fi

echo "Запуск scripts/form_dataset.py с files_dir=$1"
python scripts/form_dataset.py --files_dir="$1"
python scripts/create_yaml.py

if [ $? -eq 0 ]; then
  echo "Скрипт успешно завершен."
else
  echo "Ошибка: Скрипт завершился с ошибкой."
  exit 1
fi

if [ -z "$1" ]; then
  echo "Ошибка: Не указано имя выходной папки (например, box50)."
  echo "Использование: $0 box50"
  exit 1
fi

BOX_FOLDER=$1

# Извлекаем порог блюра из имени папки
THRESHOLD=$(echo "$BOX_FOLDER" | grep -oP '\d+')
if [ -z "$THRESHOLD" ]; then
  echo "Ошибка: Не удалось извлечь числовой порог из '$BOX_FOLDER'. Убедись, что имя содержит число, например 'box30'."
  exit 1
fi

# Блюринг
echo "Блюринг маленьких объектов с порогом $THRESHOLD..."
python scripts/blur.py --min_size=$THRESHOLD --output_dir=$BOX_FOLDER

echo "Анализ размеров bounding bbox"
python scripts/analyze_bbox_sizes.py --labels_dir="dataset/college_try"



