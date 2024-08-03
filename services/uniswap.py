import asyncio
import random
from playwright.async_api import expect
from loguru import logger
from config import AMOUNT, DEFAULT_DELAY, METAMASK_ID, USDC_BASE_ADDRESS, EYES_BASE_ADDRESS, WETH_BASE_ADDRESS
from custom_logger import Logger


class Uniswap:
    uniswap_url = 'https://app.uniswap.org/swap'

    def __init__(self, context, transaction_type: str = 'buy') -> None:
        self.context = context
        self.transaction_type = transaction_type

    async def mm_page_action(
            self, 
            mm_page, 
            method: str,
            locator_settings: list, 
            timeout: int = 20000,
            delay_between_actions: int = DEFAULT_DELAY,
        ):
        for setting in locator_settings:
            button = getattr(mm_page, method)(setting)
            await expect(button).to_be_visible(timeout=timeout)
            await button.click()

            await asyncio.sleep(delay_between_actions)

    async def login(self, page):
        logger.info("Connecting to Uniswap")

        await asyncio.sleep(3)

        await self.mm_page_action(
            mm_page=page,
            method='locator',
            locator_settings=[
                '//*[@id="swap-page"]/div/div[4]/div[2]/button/div',
                'button:has-text("MetaMask")'
            ],
            timeout=3000
        )

        try:
            context = self.context
            new_page = await context.new_page()
            await new_page.goto(f'chrome-extension://{METAMASK_ID}/home.html#')

            await self.mm_page_action(
                mm_page=new_page,
                method='get_by_test_id',
                locator_settings=[
                    'page-container-footer-next',
                    'page-container-footer-next'
                ],
                timeout=20000
            )

            await asyncio.sleep(5)

            if len(context.pages) > 1:
                await new_page.close()
            else:
                raise Exception('Count of pages is not correct...')

            logger.success('Successfully logged in!')
        except Exception as e:
            raise e
    
    async def change_chain_to_base(self):
        try:
            mm_page = await self.context.new_page()
            await mm_page.goto(f'chrome-extension://{METAMASK_ID}/home.html#')

            connect_wallet_next_btn = mm_page.get_by_test_id(test_id='confirmation-submit-button')
            await expect(connect_wallet_next_btn).to_be_visible(timeout=20000)
            await connect_wallet_next_btn.click()
            await connect_wallet_next_btn.click()
            await mm_page.close()
            logger.success('Metamask changed chain successfully!')
        except Exception as e:
            logger.error(f'Something went wrong, trying again... {e}')
            await mm_page.close()
            raise Exception("Can't change chain. Starting task again...")
    
    async def send_transaction(self):
        try:
            mm_page = await self.context.new_page()
            await mm_page.goto(f'chrome-extension://{METAMASK_ID}/home.html#')

            await self.mm_page_action(
                mm_page=mm_page,
                method='locator',
                locator_settings=[
                    '//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]',
                ]
            )
            await mm_page.close()

            logger.success('Transaction sent!')
        except Exception as e:
            logger.error(f'Something went wrong, trying again... {e}')
            await mm_page.close()
            raise Exception("Can't accept transaction. Starting task again...")
    
    async def accept_transaction(self):
        try:
            mm_page = await self.context.new_page()
            await mm_page.goto(f'chrome-extension://{METAMASK_ID}/home.html#')

            await self.mm_page_action(
                mm_page=mm_page,
                method='locator',
                locator_settings=[
                    '//*[@id="app-content"]/div/div/div/div[7]/div/div[2]/button', # max_button
                    '//*[@id="app-content"]/div/div/div/div[10]/footer/button[2]', # next
                    '//*[@id="app-content"]/div/div/div/div[11]/footer/button[2]' # confirm
                ],
                delay_between_actions=1.2,
                timeout=10000
            )

            await mm_page.close()

            logger.success('Accepted transaction!')
        except AssertionError as e:
            logger.error(f'Элемент не найден: {e}')
            logger.info("Скорее всего уже был approve токена")
            return True
        except Exception as e:
            raise e
    
    async def sign_transaction(self):
        try:
            mm_page = await self.context.new_page()
            await mm_page.goto(f'chrome-extension://{METAMASK_ID}/home.html#')

            await self.mm_page_action(
                mm_page=mm_page,
                method='locator',
                locator_settings=[
                    '//*[@id="app-content"]/div/div/div/div[5]/footer/button[2]'
                ],
                delay_between_actions=0
            )

            await mm_page.close()

            logger.success('Signed transaction!')

        except AssertionError as e:
            logger.error(f'Элемент не найден: {e}')
            logger.info("Возможно, подпись не требуется")
            return True
        except Exception as e:
            logger.error(f'Something went wrong, trying again... {e}')
            await mm_page.close()
            raise Exception("Can't sign transaction. Starting task again...")

    async def swap(self):
        uniswap_url = 'https://app.uniswap.org/swap'
        page = await self.context.new_page()
        await page.goto(uniswap_url)

        await asyncio.sleep(1.5)

        # Убираем начальное всплывающее окно, с помощью клика по рандомноу месту на экране
        await page.mouse.click(310, 687)

        await self.login(page)

        await self.mm_page_action(
            mm_page=page,
            method='locator',
            timeout=3000,
            delay_between_actions=1,
            locator_settings=['//*[@id="AppHeader"]/div[2]/nav/div/div[3]/div[1]','button:has-text("Base")'],
        )

        await self.change_chain_to_base()

        await asyncio.sleep(2)

        # Выбираем token_in
        choose_token_button = page.locator('//*[@id="swap-currency-output"]/div/div[1]/div[2]/div/button')
        await expect(choose_token_button).to_be_visible()
        await choose_token_button.click()
        
        # Выбираем token_out
        token_name_input = page.locator('#token-search-input')
        await expect(token_name_input).to_be_visible()
        await token_name_input.type(EYES_BASE_ADDRESS)

        await asyncio.sleep(1.5)

        await self.mm_page_action(
            mm_page=page,
            method='locator',
            timeout=3000,
            delay_between_actions=1,
            locator_settings=[
                '//html/body/reach-portal[4]/div[2]/div/div/div/div/div[3]/div/div/div[2]',
                '//html/body/reach-portal[4]/div[2]/div/div/div/div/div/button[1]'
            ]
        )

        await asyncio.sleep(1.5)

        if self.transaction_type == 'sell':
            await self.mm_page_action(
                mm_page=page,
                method='locator',
                timeout=1000,
                delay_between_actions=2,
                locator_settings=['//*[@id="swap-page"]/div/div[3]/div[2]/div'] # меняем токены местами
            )

        # Вводим количество для свапа
        inputs = page.get_by_placeholder('0')
        await expect(inputs.first).to_be_visible()
        await inputs.first.type(AMOUNT)

        await asyncio.sleep(3.5)

        # Свапаем токены
        await self.mm_page_action(
            mm_page=page,
            method='locator',
            timeout=1000,
            delay_between_actions=1.5,
            locator_settings=['//*[@id="swap-button"]', '//*[@id="confirm-swap-or-send"]']
        )
        
        if self.transaction_type == 'sell':
            result = await self.accept_transaction()
            await asyncio.sleep(3)

            if not result:
                await self.sign_transaction()
                await asyncio.sleep(3)

        await self.send_transaction()

        logger.info("Uniswap swapped successfully!")

        await asyncio.sleep(5)
        await self.context.close()
