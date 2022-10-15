# Аналитический телеграмм-бот для ВК (Тестовая версия, будут патчи)

Удобный аналитический бот, который поможет мониторить группы ВК, следить за реакцией пользователей и статистикой

## Вы сможете
- Собирать данные группы одной командой 
- Отслеживать статистику по периоду времени
- Смотреть топы групп по периоду времени
- Наладить автоматический мониторинг

## Установка
1. Клонируйте репозиторий с GitHub `git clone https://github.com/lowfie/VkAnalyzing.git`
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Добавьте файл `.env` в папку директорию `data`
5. Установите docker для вашей ОС

Запустите локальную БД для работы FSM в aiogram и PostgreSQL для сбора данных:
```
docker run -p 6379:6379 -d redis
docker run -p 5432:5432 -e POSTGRES_PASSWORD=123 -d postgres
```

## Конфигурация бота (.env)
```
VK_TOKEN=vk_api_token
BOT_TOKEN=telegram_api_token

USER_POSTGRES=postgres
PASSWORD_POSTGRES=123
HOST_POSTGRES=localhost
PORT_POSTGRES=5432
DATABASE_POSTGRES=postgres

PREFIX_REDIS=state_aiogram
PASSWORD_REDIS=
HOST_REDIS=localhost
PORT_REDIS=6379
DATABASE_REDIS=0
```

## Дополнительные источники
- **Инструкция для получения VK_TOKEN [*здесь*](https://dvmn.org/encyclopedia/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/)**
- **Получить токен на VK_TOKEN [*здесь*](https://dev.vk.com/)**
- **Инструкция для получения TELEGRAM_TOKEN [*здесь*](https://web7.pro/kak-poluchit-token-bota-telegram-api/)**

