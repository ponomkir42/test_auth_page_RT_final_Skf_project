from pages.auth_page import MainPage
from pages.locators import *
from settings import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument("--start-maximized")
    return chrome_options


def test_auth_for_crush(selenium):
    """Проверка поведения сайта при вводе в поля логина и пароля строки длиной >2500 символов, в данном тесте также
    сохраняем скриншот с уникальным именем, если вдруг будет отличное от падения страницы с ошибкой internal server
    error"""
    page = MainPage(selenium)
    page.enter_username(InvalidData.login*250)
    page.enter_pass(InvalidData.password*250)
    page.btn_click()

    page.driver.save_screenshot(f'{time.time()}.png')

    assert page.find_elem(*internal_error_message_text).text == 'Internal Server Error'


def test_auth_by_email_positive(selenium):
    """Авторизация пользователя с валидным email и паролем"""
    page = MainPage(selenium)
    page.enter_username(AuthEmail.email)
    page.enter_pass(AuthEmail.password)
    page.btn_click()

    assert page.get_relative_link() == '/account_b2c/page'


def test_auth_by_email_negative(selenium):
    """Авторизация пользователя с невалидным сочетанием email/пароль"""
    page = MainPage(selenium)
    page.enter_username(AuthEmail.email)
    page.enter_pass(InvalidData.password)
    page.btn_click()

    assert page.get_relative_link() != '/account_b2c/page'
    assert page.find_elem(*wrong_log_pass_message).text == 'Неверный логин или пароль'


def test_auth_by_phone_positive(selenium):
    """Авторизация пользователя с валидным номером телефона и паролем"""
    page = MainPage(selenium)
    page.enter_username(AuthPhone.phone)
    page.enter_pass(AuthPhone.password)
    page.btn_click()

    assert page.get_relative_link() == '/account_b2c/page'


def test_auth_by_phone_negative(selenium):
    """Авторизация пользователя с невалидным сочетанием email/пароль"""
    page = MainPage(selenium)
    page.enter_username(AuthPhone.phone)
    page.enter_pass(InvalidData.password)
    page.btn_click()

    assert page.get_relative_link() != '/account_b2c/page'
    assert page.find_elem('xpath', '//*[@id="page-right"]/div/div/p').text == 'Неверный логин или пароль'


def test_auth_by_login_negative(selenium):
    """Авторизация пользователя с невалидным сочетанием логин/пароль. Проверить валидное сочетание нет возможности,
    так как логин выдается только при оформлении договора на оказание услуг связи с ростелекомом """
    page = MainPage(selenium)
    page.enter_username(InvalidData.login)
    page.enter_pass(InvalidData.password)
    page.btn_click()

    assert page.get_relative_link() != '/account_b2c/page'
    assert page.find_elem('xpath', '//*[@id="page-right"]/div/div/p').text == 'Неверный логин или пароль'


def test_change_placeholder_text(selenium):
    """Проверка смены текста плейсхолдера при смене типа данных (почта, телефон, логин, номер договора), вводимых в
    поле username """
    page = MainPage(selenium)
    page.enter_username(AuthEmail.email)
    # вводим любой пароль, чтобы обновился плейсхолдер
    page.enter_pass('123')

    assert page.placeholder.text == 'Электронная почта'

    # перезагружаем страницу (команда .clear() по отношению к полю ввода username не работает почему-то)
    page = MainPage(selenium)
    page.enter_username('89874514785')
    page.enter_pass('123')

    assert page.placeholder.text == 'Мобильный телефон'

    page = MainPage(selenium)
    page.enter_username('mytestlogin')
    page.enter_pass('123')

    assert page.placeholder.text == 'Логин'

    page = MainPage(selenium)
    page.enter_username('123456789123')
    page.enter_pass('123')

    assert page.placeholder.text == 'Лицевой счёт'


def test_forget_password_link(selenium):
    """Проверка перехода по ссылке Забыл пароль"""
    page = MainPage(selenium)
    page.forget_password_link.click()

    assert page.find_elem(*restore_passw_text).text == 'Восстановление пароля'


def test_registration_link(selenium):
    """Проверка перехода по ссылке Зарегистрироваться"""
    page = MainPage(selenium)
    page.registration_link.click()

    assert page.find_elem(*registr_page_text).text == 'Регистрация'


def test_chat_open(selenium):
    """Открытие и авторизация в чате, проверка получения вступительного сообщения в чате"""
    page = MainPage(selenium)
    page.find_elem(*widget_bar).click()
    page.find_elem(*username_chat).send_keys('Иван')
    page.find_elem(*phone_chat).send_keys('9856815900')
    page.find_elem(*button_enter_chat).click()

    # добавлено явное ожидание вступительного сообщения, так как окно чата загружается не сразу. А так как данный метод
    # возвращает True или False в зависимости от того, появился требуемый текст или нет, его удобно использовать
    # для проверки
    assert WebDriverWait(page.driver, 5).until(EC.text_to_be_present_in_element(chat_greetings, chat_greetings_text))


def test_auth_vk_button(selenium):
    """Проверка кнопки авторизации пользователя при помощи VK ID"""
    page = MainPage(selenium)
    page.vk_button.click()

    assert page.get_base_url() == 'oauth.vk.com'


def test_auth_ok_button(selenium):
    """Проверка кнопки авторизации пользователя при помощи сайта Одноклассники"""
    page = MainPage(selenium)
    page.ok_button.click()

    assert page.get_base_url() == 'connect.ok.ru'


def test_auth_mailru_button(selenium):
    """Проверка кнопки авторизации пользователя при помощи сайта Одноклассники"""
    page = MainPage(selenium)
    page.mailru_button.click()

    assert page.get_base_url() == 'connect.mail.ru'


def test_auth_google_button(selenium):
    """Проверка кнопки авторизации пользователя при помощи Google"""
    page = MainPage(selenium)
    page.google_botton.click()

    assert page.get_base_url() == 'accounts.google.com'


def test_auth_ya_button(selenium):
    """Проверка кнопки авторизации пользователя при помощи Yandex"""
    page = MainPage(selenium)
    page.ya_button.click()

    assert page.get_base_url() == 'passport.yandex.ru'


def test_agreement_links(selenium):
    """Проверка открытия ссылок, ведущих на страницу пользовательского соглашения. При нажатии на ссылку открывается
    новая вкладка, проверяется заголовок вкладки, затем она закрывается """
    page = MainPage(selenium)
    original_window = page.driver.current_window_handle
    page.find_elem(*link_user_agreement_auth_form).click()
    WebDriverWait(page.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in page.driver.window_handles:
        if window_handle != original_window:
            page.driver.switch_to.window(window_handle)
            break
    window_title = page.driver.execute_script("return window.document.title")

    assert window_title == 'User agreement'

    page.driver.close()
    page.driver.switch_to.window(original_window)
    page.find_elem(*link_user_agreement_footer_first).click()
    WebDriverWait(page.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in page.driver.window_handles:
        if window_handle != original_window:
            page.driver.switch_to.window(window_handle)
            break

    assert window_title == 'User agreement'

    page.driver.close()
    page.driver.switch_to.window(original_window)
    page.find_elem(*link_user_agreement_footer_second).click()
    WebDriverWait(page.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in page.driver.window_handles:
        if window_handle != original_window:
            page.driver.switch_to.window(window_handle)
            break

    assert window_title == 'User agreement'


