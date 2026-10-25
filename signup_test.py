import os
import random
import string
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("TEST_URL", "http://localhost:3000/signup")
RUNS = min(int(os.environ.get("RUNS", "1")), 5)  # safety cap
HEADLESS = os.environ.get("HEADLESS", "1") == "1"


def rand_str(n=6):
    return "".join(random.choices(string.ascii_lowercase, k=n))


def make_driver():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=opts)


def run_signup_test(i):
    driver = make_driver()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get(BASE_URL)

        # Field names apni site ke HTML se inspect karke badal lena
        wait.until(EC.presence_of_element_located((By.NAME, "fullname"))).send_keys(f"Test {rand_str()}")
        driver.find_element(By.NAME, "phone").send_keys("9" + "".join(random.choices(string.digits, k=9)))
        driver.find_element(By.NAME, "password").send_keys("TestPass@123")

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)
        print(f"[{i + 1}/{RUNS}] submitted -> {driver.current_url}")
    except Exception as e:
        driver.save_screenshot(f"error_{i + 1}.png")
        print(f"[{i + 1}/{RUNS}] error: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    for i in range(RUNS):
        run_signup_test(i)
        time.sleep(5)
