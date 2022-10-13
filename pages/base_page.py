from urllib.parse import urlparse


class BasePage(object):
    def __init__(self, driver, url, timeout=10):
        self.driver = driver
        self.url = url
        self.driver.implicitly_wait(timeout)

    # метод, который будет выводить относительный путь url без домена (очень полезная либа)
    def get_relative_link(self):
        url = urlparse(self.driver.current_url)
        return url.path

    def get_base_url(self):
        url = urlparse(self.driver.current_url)
        return url.hostname
