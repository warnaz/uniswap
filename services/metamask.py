import asyncio
from custom_logger import Logger
from playwright.async_api import expect
from config import MM_PASSWORD


class MetaMask(Logger):
    def __init__(self, mnemonic, context):
        self.mnemonic = mnemonic
        self.context = context
        super().__init__()

    async def connect_metamask_extension(self):
        await asyncio.sleep(5)
        self.logger.info("Connecting to Metamask")
        background = self.context.service_workers[0]
        if not background:
            background = self.context.wait_for_event("serviceworker")

        extension_id = background.url.split("/")[2]
        titles = [await p.title() for p in self.context.pages]
        while 'MetaMask' not in titles:
            titles = [await p.title() for p in self.context.pages]
        mm_page = self.context.pages[1]
        await mm_page.wait_for_load_state()

        checkbox = mm_page.locator('//*[@id="onboarding__terms-checkbox"]')
        await mm_page.wait_for_load_state(state='domcontentloaded')
        await checkbox.click()

        create_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-import-wallet')
        await expect(create_wallet_btn).to_be_enabled()
        await create_wallet_btn.click()

        i_dont_agree_btn = mm_page.get_by_test_id(test_id='metametrics-no-thanks')
        await expect(i_dont_agree_btn).to_be_attached()
        await i_dont_agree_btn.click()

        for i in range(len(self.mnemonic.split())):
            await mm_page.get_by_test_id(test_id=f'import-srp__srp-word-{i}').fill(self.mnemonic.split()[i])

        confirm_btn = mm_page.get_by_test_id(test_id='import-srp-confirm')
        await expect(confirm_btn).to_be_enabled()
        await confirm_btn.click()

        passwd_1 = mm_page.get_by_test_id(test_id='create-password-new')
        passwd_2 = mm_page.get_by_test_id(test_id='create-password-confirm')
        checkbox = mm_page.get_by_test_id(test_id='create-password-terms')
        create_wallet_btn = mm_page.get_by_test_id(test_id='create-password-import')
        await expect(passwd_1).to_be_attached()
        await passwd_1.fill(MM_PASSWORD)
        await passwd_2.fill(MM_PASSWORD)
        await checkbox.click()

        await expect(create_wallet_btn).to_be_enabled()
        await create_wallet_btn.click()

        create_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-complete-done')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        create_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-next')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        create_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-done')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()
        self.logger.success('Metamask connected!')
        # await mm_page.close()
