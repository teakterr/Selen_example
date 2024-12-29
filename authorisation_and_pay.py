from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import unittest


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.link = "https://online.sbis.ru"
        self.loginstr = 'qwerty'
        self.password = '1234'
        self.browser.get(self.link)
    
    def tearDown(self):
        self.browser.quit()

    def login(self):
        login_input=WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.controls-InputBase__nativeField[type='text']"))
        )
        time.sleep(1)
        login_input = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.controls-InputBase__nativeField[type='text']"))
        )
        time.sleep(2)
        try:
            login_input.send_keys(self.loginstr)
        except:
            print('Stale')
            self.browser.find_element(By.CSS_SELECTOR, "input.controls-InputBase__nativeField[type='text']").click()
        button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='auth-AdaptiveLoginForm__checkSignInTypeButton']>span"))
        )
        button.click()
        
        password_input = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[type='password'][inputmode='text']"))
        )
        password_input.send_keys(self.password)
        
        sign_in_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='auth-AdaptiveLoginForm__signInButton']>span"))
        )
        sign_in_button.click()

    def open_shift(self):
        open_shift = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='Открыть смену']"))
        )
        time.sleep(2)
        open_shift = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Открыть смену']"))
        )
        actions = ActionChains(self.browser)
        actions.move_to_element(open_shift).perform()
        open_shift.click()


class TestAuthor(BaseTest):
    def test_wrong_credentials(self):
        self.login()
        error_message = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.controls-fontsize-3xl"))
        )
        self.assertEqual(error_message.text, "Неверный логин или пароль")


class TestPayRetail(BaseTest):
    def test_pay(self):
        demo_button = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='Попробовать демо']"))
        )
        time.sleep(1)
        demo_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Попробовать демо']"))
        )
        time.sleep(2)
        demo_button.click()
        
        for_retail = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Для магазинов']"))
        )
        for_retail.click()
        
        front_ret = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Фронт-офис']"))
        )
        front_ret.click()
        
        self.open_shift()
        time.sleep(3)
        self.open_shift()
        time.sleep(3)
        self.open_shift()
        time.sleep(3)
        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span[title='Закрыть']"))
            ).click()
        except:
            print("Without clue")
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[title='Туалетная вода «Букет России», зел. чай, 40мл ']"))
        )
        toilet_water = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[title='Туалетная вода «Букет России», зел. чай, 40мл ']"))
        )
        toilet_water.click()
        
        message = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='Продажа маркированного товара невозможна']"))
        )
        self.assertEqual(message.text, 'Продажа маркированного товара невозможна', 'ERROR, result='+message.text)


if __name__ == "__main__":
    unittest.main()