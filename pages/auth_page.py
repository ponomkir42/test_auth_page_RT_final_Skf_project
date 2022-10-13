from .base_page import BasePage
from .locators import AuthLocators

import time
import os


class MainPage(BasePage):
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c' \
              '&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid& '
        driver.get(url)

        self.username = driver.find_element(*AuthLocators.auth_username)
        self.password = driver.find_element(*AuthLocators.auth_password)
        self.auth_btn = driver.find_element(*AuthLocators.auth_button)
        self.placeholder = driver.find_element(*AuthLocators.placeholder)
        self.forget_password_link = driver.find_element(*AuthLocators.forget_passw_link)
        self.registration_link = driver.find_element(*AuthLocators.registr_link)
        self.vk_button = driver.find_element(*AuthLocators.vk_auth_button)
        self.ok_button = driver.find_element(*AuthLocators.ok_auth_button)
        self.mailru_button = driver.find_element(*AuthLocators.mailru_auth_button)
        self.google_botton = driver.find_element(*AuthLocators.google_auth_button)
        self.ya_button = driver.find_element(*AuthLocators.ya_auth_button)

    def enter_username(self, value):
        self.username.send_keys(value)

    def enter_pass(self, value):
        self.password.send_keys(value)

    def btn_click(self):
        self.auth_btn.click()

    def refresh_page(self):
        self.driver.refresh()

    def find_elem(self, by, location):
        return self.driver.find_element(by, location)

