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

docker --version
docker compose version

## 3 Настройка переменных окружения (рекомендуется)

Сейчас пароль Redis захардкожен в docker-compose.yml (и в command --requirepass ...). 

В десятой строке указывается пароль дял доступа к Redis из вне

*Важно:* в текущем compose также создаётся сеть pray_rep_app_network.

Эта сеть должна быть общей для остальных сервисов.

## 4 Сборка и запуск Redis (сначала всегда Redis!)

В вашем README сейчас команда указана с опечаткой up -b. Должно быть -d (detach). 

```bash
sudo docker compose up -d
```

Проверка:
```bash
docker ps
docker network ls | grep pray_rep_app_network
```