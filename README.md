# АИС BGConsult

Документация: https://papr1ka.github.io/BGConsult/

Структура проекта:

```bash
.
├── back                    - Серверная часть приложения
│   ├── app
│   ├── Dockerfile
│   └── requirements.txt    Зависимости для сервера, поддерживать в актуальном состоянии!
├── bot                     - Бот приложения
│   ├── config
│   ├── handlers
│   ├── keyboards
│   ├── Dockerfile          - Фай
│   └── requirements.txt    Зависимости для бота, поддерживать в актуальном состоянии!
├── docs                    - Документация разработчика
│   ├── build
│   └── source
└── system_docs             - Справочная информация про систему
```

Запуск:

Создайте файл .env в корневой директории со следующим содержимым:

```bash
    BOT_TOKEN={Ваш токен}
```

Или установите переменную окружения в docker-compose.yml вручную

Для развёртывания:

```bash
    docker compose up
```

Для развёртывания в процессе разработки:

```bash
    docker compose up --no-deps --build
```


Руководство пользователя:

[Руководство тут](./system_docs/user_guide/guide.md)

Оставить обратную связь:

https://github.com/Papr1ka/BGConsult/issues
