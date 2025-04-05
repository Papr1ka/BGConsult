Создание документации
======================

Чтобы создать документацию локально, необходимо:

1. Создать виртуальное окружение
2. Установить зависимости из back/requirements.txt
3. Установить зависимость из bot/requirements.txt
4. Установить библиотеки sphinx и furo
5. Собрать документацию



.. code-block:: bash

    python -m venv venv
    source ./venv/bin/activate # или аналог для windows
    python -m pip install -r ./back/requirements.txt
    python -m pip install -r ./bot/requirements.txt
    python -m pip install sphinx furo
    # сборка документации
    cd docs
    sphinx-apidoc build/ ../
    make html
