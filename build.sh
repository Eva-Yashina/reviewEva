#!/bin/bash

# Убедимся, что Docker запущен
if ! docker info > /dev/null 2>&1; then
  echo "Docker не запущен. Пожалуйста, запустите Docker и попробуйте снова."
  exit 1
fi

# Имя образа
IMAGE_NAME="app"

# Сборка Docker образа
echo "Сборка Docker образа..."
docker build -t $IMAGE_NAME .

# Проверка успешности сборки
if [ $? -ne 0 ]; then
  echo "Ошибка при сборке Docker образа."
  exit 1
fi

# Запуск контейнера
echo "Запуск контейнера..."
docker run -p 5000:5000 $IMAGE_NAME
