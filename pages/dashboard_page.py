# pages/dashboard_page.py
# Latihan 3.1 — DashboardPage
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    URL = 'https://the-internet.herokuapp.com/secure'

    # ── Locators ──────────────────────────────────────────
    LOGOUT_BTN  = (By.CSS_SELECTOR, "a[href='/logout']")
    FLASH_MSG   = (By.ID, 'flash')
    PAGE_HEADER = (By.CSS_SELECTOR, 'h2')

    # ── Actions ───────────────────────────────────────────
    def logout(self):
        self.logger.info('Klik tombol Logout')
        self.click(self.LOGOUT_BTN)

    # ── Assertion Helpers ─────────────────────────────────
    def is_on_dashboard(self) -> bool:
        try:
            url_ok    = 'secure' in self.get_current_url()
            header_ok = 'Secure Area' in self.get_text(self.PAGE_HEADER)
            return url_ok and header_ok
        except Exception:
            return False

    def get_flash_message(self) -> str:
        return self.get_text(self.FLASH_MSG)
