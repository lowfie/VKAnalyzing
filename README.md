# Аналитический телеграмм-бот для ВК

Удобный аналитический бот, который поможет мониторить группы ВК, следить за реакцией пользователей и статистикой

- **Отдельная благодарность моему куратору за помощь - [*куратор*](https://github.com/n05tr0m0)**

## Вы сможете
- Собирать данные группы одной командой 
- Отслеживать статистику по периоду времени
- Смотреть топы групп по периоду времени
- Наладить автоматический мониторинг

## Установка
1. Клонируйте репозиторий с GitHub `git clone https://github.com/lowfie/VkAnalyzing.git`
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Добавьте файл `.env` в корневую директорию
5. Установите docker для вашей ОС

Также необходимо скачать веса для модели нейросети
```
python -m dostoevsky download fasttext-social-network-model
```
Если у вас Windows, то возможны проблемы с установкой FastText 
- **Можете найти FastText [*здесь*](https://www.lfd.uci.edu/~gohlke/pythonlibs/)**

Базы данных:
- Запустите (брокер) Redis для работы FSM в aiogram
- Также (хранилище) PostgreSQL для сбора данных:
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
- **Получить VK_TOKEN [*здесь*](https://dev.vk.com/)**
- **Инструкция для получения TELEGRAM_TOKEN [*здесь*](https://web7.pro/kak-poluchit-token-bota-telegram-api/)**

