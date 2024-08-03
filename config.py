MM_PASSWORD = '123456789'  # Пароль для метамаска (любой)
HIDEN_RUN = False  # Запуск в фоне или нет
EXTENTION_PATH = '' # путь до расширения Metamask
METAMASK_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'


def get_data(file: str):
    with open(f'data/{file}', 'r') as file:
        return file.read()


MNEMONIK = get_data('mnemonics.txt')
PROXIES = get_data('proxies.txt')

# Для Debug режима, оставить на True
METAMASK = True
UNISWAP = True

# Настройки
DEFAULT_DELAY = 1.5
SLOW_MO_MODE = 50 # Насколько быстро будет работать скрипт
AMOUNT = '0.0001'
TRANSACTION_TYPE = 'buy' # buy/sell (покупка/продажа)

# Адреса в Base сети
WETH_BASE_ADDRESS = "0x4200000000000000000000000000000000000006"
USDC_BASE_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
USDT_BASE_ADDRESS = "0xfde4c96c8593536e31f229ea8f37b2ada2699bb2"
EYES_BASE_ADDRESS = "0x466205989D219555716579881B7cE8207F4c636e"
