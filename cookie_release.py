import sys
import termios
import tty
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import threading
from queue import Queue
from datetime import timedelta

def clicker(stop_event, result_queue):
    start_time = time.time()
    link = 'https://orteil.dashnet.org/cookieclicker/'
    browser = webdriver.Chrome()
    browser.get(link)
    WebDriverWait(browser, 25).until(
        EC.visibility_of_element_located((By.ID, "langSelect-RU"))
    )
    WebDriverWait(browser, 25).until(
        EC.element_to_be_clickable((By.ID, "langSelect-RU"))
    ).click()
    i = 0
    WebDriverWait(browser, 25).until(
        EC.visibility_of_element_located((By.ID, "bigCookie"))
    )
    main_butt = WebDriverWait(browser, 25).until(
        EC.element_to_be_clickable((By.ID, "bigCookie"))
    )

    while not stop_event.is_set():
        i += 1
        try:
            main_butt.click()
        except:
            pass
    browser.quit()
    result_queue.put((i, start_time))  
def get_keypress():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
stop_event = threading.Event()
result_queue = Queue()
click_thread = threading.Thread(target=clicker, args=(stop_event, result_queue))
click_thread.start()
print("Для остановки нажмите s")
while True:
    key = get_keypress()
    if key == 's':
        stop_event.set()
        break
click_thread.join()
result = result_queue.get()  
clicks_count, start_time = result  
end_time = time.time()
res_time = end_time - start_time
time_str = str(timedelta(seconds=int(res_time)))
print(f'Кликов: {clicks_count}, время работы: {time_str}')