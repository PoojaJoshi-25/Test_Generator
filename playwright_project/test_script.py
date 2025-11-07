from playwright.sync_api import Page, expect
import pytest
from actions import LoginPageActions

BASE_URL = "https://opensource-demo.orangehrmlive.com"

def test_successful_login(page: Page):
    login_page = LoginPageActions(page)
    login_page.navigate()
    login_page.login("Admin", "admin123")
    # Assuming successful login redirects to a page with a specific element. Adapt as needed.
    page.wait_for_selector(".oxd-sidepanel")
    assert page.url != BASE_URL # check redirect happened

def test_invalid_login(page: Page):
    login_page = LoginPageActions(page)
    login_page.navigate()
    login_page.login("InvalidUser", "InvalidPassword")
    assert "Invalid credentials" in login_page.get_error_message_text()

def test_empty_username_login(page: Page):
     login_page = LoginPageActions(page)
     login_page.navigate()
     login_page.login("", "admin123")
     assert "Username cannot be empty" in login_page.get_error_message_text() #adapt error message as required
