Запуск
======

Создайте файл .env в корневой директории со следующим содержимым:

.. code-block:: bash

    BOT_TOKEN={Ваш токен}

Или установите переменную окружения в docker-compose.yml вручную

Для развёртывания:

.. code-block:: bash

    docker compose up

Для развёртывания в процессе разработки:

.. code-block:: bash

    docker compose up --no-deps --build

