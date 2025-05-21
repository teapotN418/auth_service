### Запуск проекта с Doker
2.1.1 Добавляете .env файл в папку

2.1.2 Создаете и запускаете контейнер через терминал:
```sh
sudo docker-compose up -d
```

2.1.3 Применяете миграции в базе данных:
```sh
sudo docker exec -it my_fastapi_users alembic upgrade head
```

2.1.4 Сервис доступен по адресу: http://0.0.0.0:8000/

2.1.5 Запускаете тесты (желательно применять pytest-env):
```sh
docker exec -it my_fastapi_users pytest --cov
```