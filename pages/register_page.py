# pages/register_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class RegisterPage(BasePage):
    URL = 'https://demoqa.com/register'

    # ── Locators ──────────────────────────────────────────
    USERNAME_FIELD = (By.ID, 'userName')
    EMAIL_FIELD    = (By.ID, 'userEmail')
    PASSWORD_FIELD = (By.ID, 'password')
    CONFIRM_FIELD  = (By.ID, 'userPassword')
    REGISTER_BTN   = (By.ID, 'register')
    SUCCESS_MSG    = (By.ID, 'output')

    # ── Actions ───────────────────────────────────────────
    def navigate(self):
        self.open(self.URL)

    def fill_form(self, username, email, password, confirm_password):
        if username:         self.type(self.USERNAME_FIELD, username)
        if email:            self.type(self.EMAIL_FIELD, email)
        if password:         self.type(self.PASSWORD_FIELD, password)
        if confirm_password: self.type(self.CONFIRM_FIELD, confirm_password)

    def click_register(self):
        self.click(self.REGISTER_BTN)

    def register(self, username, email, password, confirm_password):
        """High-level method: navigasi → isi form → submit"""
        self.navigate()
        self.fill_form(username, email, password, confirm_password)
        self.click_register()

    # ── Assertion Helpers ─────────────────────────────────
    def is_registration_successful(self) -> bool:
        try:
            wait = WebDriverWait(self.driver, 5)
            el   = wait.until(EC.visibility_of_element_located(self.SUCCESS_MSG))
            return 'successfully' in el.text.lower()
        except Exception:
            return False

    def is_registration_failed(self) -> bool:
        return not self.is_registration_successful()
