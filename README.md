# Сервис очереди Redis

## 1 Скачать код с Git и перейти на ветку Redis
```bash
git clone git@github.com:Zakharov-Ilya-Proger/pray_rep.git
cd pray_rep

git fetch --all
git checkout redis-prod
```
## 2 Установка Docker на сервере

Для установки и запуска системы docker а сервер перейдите по [ссылке](https://docs.docker.com/engine/install/) и настройте.

Минимально проверьте, что всё ок:
```bash
docker --version
docker compose version
```
## 3 Настройка переменных окружения (рекомендуется)

Сейчас пароль Redis захардкожен в docker-compose.yml 

Пропишите в поле на 10 строчке пароль, по которому Redis будет доступен

Эта сеть должна быть общей для остальных сервисов.

## 4 Сборка и запуск Redis (сначала всегда Redis!)
```bash
sudo docker compose up -d
```

Проверка:
```bash
docker ps
docker network ls | grep pray_rep_app_network
```