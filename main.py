import asyncio
from proxy import Proxy
from runner import Runner
from config import METAMASK, MNEMONIK, UNISWAP, PROXIES


async def runner():
    uniswap_runner = Runner(
        is_uniswap=UNISWAP, 
        is_metamask=METAMASK, 
        mnemonic=MNEMONIK,
        proxy=None # Чтобы использовать прокси пропишите так: Proxy(PROXIES)
    )

    await uniswap_runner.run_task_ui()


if __name__ == "__main__":
    asyncio.run(runner())
