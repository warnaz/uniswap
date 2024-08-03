import pyuseragents
from playwright.async_api import async_playwright

from config import HIDEN_RUN, EXTENTION_PATH, SLOW_MO_MODE, TRANSACTION_TYPE
from proxy import Proxy
from services.metamask import MetaMask
from services.uniswap import Uniswap


class Runner:
    def __init__(self, is_uniswap: bool, is_metamask: bool, mnemonic: str, proxy: Proxy = None) -> None:
        self.is_uniswap = is_uniswap
        self.is_metamask = is_metamask
        self.proxy = proxy
        self.mnemonic = mnemonic

    async def run_task_ui(self):
        credentials, ip_port = self.proxy.w3_proxy.split('@') if self.proxy else ('', '')
        username, password = credentials[7:].split(':') if credentials else ('', '')

        async with async_playwright() as playwright:
            chromium = playwright.chromium
            user_agent = pyuseragents.random()
            context_args = ['--disable-blink-features=AutomationControlled',
                            f"--disable-extensions-except={EXTENTION_PATH}",
                            f"--load-extension={EXTENTION_PATH}"] if self.is_metamask else None

            if HIDEN_RUN:
                context_args += ["--headless=new"]
            context = await chromium.launch_persistent_context('',
                                                               headless=False,
                                                               proxy={
                                                                   'server': f'http://{ip_port}',
                                                                   'username': username,
                                                                   'password': password
                                                               } if self.proxy else None,
                                                               args=context_args,
                                                               user_agent=user_agent,
                                                               slow_mo=SLOW_MO_MODE)

            # Connect to Metamask
            if self.is_metamask:
                metamask = MetaMask(
                            mnemonic=self.mnemonic,
                            context=context)
                await metamask.connect_metamask_extension()

            # Swap on Uniswap
            if self.is_uniswap:
                uniswap = Uniswap(context, transaction_type=TRANSACTION_TYPE)
                await uniswap.swap()

            await context.close()
