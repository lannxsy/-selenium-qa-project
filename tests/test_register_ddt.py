# tests/test_register_ddt.py
# Latihan 4.1 — DDT Register dari CSV + Auto Screenshot saat FAIL
import os
import csv
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

def load_csv(filename: str) -> list:
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

# ── Page Object: RegisterPage ─────────────────────────────────────────────────
class RegisterPage(BasePage):
    URL            = 'https://demoqa.com/register'
    USERNAME_FIELD = (By.ID, 'userName')
    EMAIL_FIELD    = (By.ID, 'userEmail')
    PASSWORD_FIELD = (By.ID, 'password')
    CONFIRM_FIELD  = (By.ID, 'userPassword')
    REGISTER_BTN   = (By.ID, 'register')
    SUCCESS_MSG    = (By.ID, 'output')

    def navigate(self):
        self.open(self.URL)

    def fill_form(self, username, email, password, confirm_password):
        if username: self.type(self.USERNAME_FIELD, username)
        if email:    self.type(self.EMAIL_FIELD, email)
        if password: self.type(self.PASSWORD_FIELD, password)
        if confirm_password: self.type(self.CONFIRM_FIELD, confirm_password)

    def click_register(self):
        self.click(self.REGISTER_BTN)

    def is_registration_successful(self) -> bool:
        try:
            wait = WebDriverWait(self.driver, 5)
            el   = wait.until(EC.visibility_of_element_located(self.SUCCESS_MSG))
            return 'successfully' in el.text.lower()
        except Exception:
            return False

    def register(self, username, email, password, confirm_password):
        self.navigate()
        self.fill_form(username, email, password, confirm_password)
        self.click_register()

# ── Test DDT ──────────────────────────────────────────────────────────────────
class TestRegisterDDT:

    @pytest.mark.parametrize(
        'row',
        load_csv('register_data.csv'),
        ids=[r['description'] for r in load_csv('register_data.csv')],
    )
    def test_register(self, driver, row):
        page = RegisterPage(driver)
        page.register(
            username         = row['username'],
            email            = row['email'],
            password         = row['password'],
            confirm_password = row['confirm_password'],
        )
        if row['expected'].upper() == 'PASS':
            assert page.is_registration_successful(), \
                f"Harus BERHASIL — {row['description']}"
        else:
            assert not page.is_registration_successful(), \
                f"Harus GAGAL — {row['description']}"
