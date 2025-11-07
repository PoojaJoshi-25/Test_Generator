from playwright.sync_api import Page, expect
import pytest
from locators import LoginPageLocators
from config import BASE_URL

class LoginPageActions:
    def __init__(self, page: Page):
        self.page = page
        self.locators = LoginPageLocators()

    def navigate(self):
        self.page.goto(BASE_URL)

    def enter_username(self, username: str):
        self.page.fill(self.locators.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        self.page.fill(self.locators.PASSWORD_INPUT, password)

    def click_login_button(self):
        self.page.click(self.locators.LOGIN_BUTTON)

    def get_error_message_text(self):
        return self.page.inner_text(self.locators.LOGIN_ERROR_MESSAGE)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()