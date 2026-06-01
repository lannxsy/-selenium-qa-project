# tests/test_logout.py
# Latihan 3.1 — Test Login → Dashboard → Logout
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLogout:

    # TC-LOGOUT-001
    def test_after_login_user_is_on_dashboard(self, login_page):
        login_page.login('tomsmith', 'SuperSecretPassword!')
        dashboard = DashboardPage(login_page.driver)
        assert dashboard.is_on_dashboard(), \
            'Setelah login, user seharusnya berada di Dashboard (Secure Area)'

    # TC-LOGOUT-002
    def test_user_can_logout(self, login_page):
        login_page.login('tomsmith', 'SuperSecretPassword!')
        dashboard = DashboardPage(login_page.driver)
        assert dashboard.is_on_dashboard(), 'Prasyarat gagal: user belum di Dashboard'
        dashboard.logout()
        assert '/login' in login_page.get_current_url(), \
            'Setelah logout, URL harus mengandung /login'

    # TC-LOGOUT-003
    def test_logout_shows_flash_message(self, login_page):
        login_page.login('tomsmith', 'SuperSecretPassword!')
        dashboard = DashboardPage(login_page.driver)
        dashboard.logout()
        msg = login_page.get_flash_message()
        assert 'logged out' in msg.lower(), \
            f'Flash message setelah logout tidak sesuai: {msg}'

    # TC-LOGOUT-004
    def test_cannot_access_secure_after_logout(self, login_page):
        login_page.login('tomsmith', 'SuperSecretPassword!')
        dashboard = DashboardPage(login_page.driver)
        dashboard.logout()
        dashboard.open(DashboardPage.URL)
        assert '/login' in login_page.get_current_url(), \
            'Akses /secure setelah logout harus di-redirect ke /login'
