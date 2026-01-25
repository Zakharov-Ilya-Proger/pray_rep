# API Сервис для добавления в Redis Queue 

## 1 Скачать код с Git и перейти на ветку Worker

```bash
git clone git@github.com:Zakharov-Ilya-Proger/pray_rep.git
cd pray_rep

git fetch --all
git checkout api-prod
```

## 2 Установка Docker на сервере

Для установки и запуска системы docker а сервер перейдите по [ссылке](https://docs.docker.com/engine/install/) и настройте.

## 3 Переменные окружения (.env)

Сервису нужны следующие переменные окружения: 

```bash
WORKERS=2
QUEUE_KEY=audio_queue
REDIS=redis://:<REDIS_PASSWORD>@redis-container:6379/0
API_PASS=change_me
```
Примечание по REDIS_URL: если Redis поднят в той же docker-сети, то хост можно указывать как имя контейнера Redis (у вас redis-container). 

## 4 Сборка и запуск (Redis должен уже работать)

_Убедитесь, что сервис Redis уже работает._

Так же проверьте какую сеть создал контейнер Redis

```bash
docker inspect --format='{{.NetworkSettings.Networks}}' redis-container
```

Приблизительный вывод

```
map[pray_rep_pray_rep_app_network:0xc00031e5a0]
```

Важно проверить, чтобы во всех полях с network было указано выведенное название

```
pray_rep_pray_rep_app_network
```

Важно про сеть: worker-сервис должен подключаться к той же сети pray_rep_app_network. Если у вас отдельный docker-compose.yml в worker-ветке — обычно сеть делают external: true и подключают сервис к ней:

```bash
networks:
  pray_rep_app_network:
    external: true
```

Дальше:
```bash
sudo docker compose up -d
```