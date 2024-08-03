# Uniswap with Playwright

Этот проект предназначен для автоматизации операций с Uniswap с помощью Playwright, чтобы торговать низколиквидными активами.

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/warnaz/uniswap.git
    ```

2. Установите необходимые зависимости:
    ```bash
    pip install -r req.txt
    ```

## Настройка

1. Заполните файл `config.py`:

    ```python
    EXTENTION_PATH = ''         # путь до расширения Metamask
    DEFAULT_DELAY = 1.5         # время задержки между действиями
    SLOW_MO_MODE = 50           # Насколько быстро будет работать скрипт
    AMOUNT = '0.0001'           # количество токенов для торговли
    TRANSACTION_TYPE = 'buy'    # buy/sell (покупка/продажа)
    ```

2. Заполните файлы в директории `data`:
    - `data/mnemonics.txt`: список мнемонических фраз, каждая на новой строке.
    - `data/proxies.txt`: список прокси, если они необходимы, каждая на новой строке.

## Использование

Для запуска скрипта выполните команду:

```bash
python main.py