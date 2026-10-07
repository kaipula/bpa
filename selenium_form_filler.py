import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.selenium.dev/selenium/web/web-form.html"

with open("form_data.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

driver = webdriver.Chrome()
driver.maximize_window()

for i, row in enumerate(rows, 1):
    driver.get(URL)

    driver.find_element(By.NAME, "my-text").send_keys(row["name"])
    driver.find_element(By.NAME, "my-password").send_keys(row["password"])
    driver.find_element(By.NAME, "my-textarea").send_keys(row["comments"])
    Select(driver.find_element(By.NAME, "my-select")).select_by_visible_text(row["option"])

    date_box = driver.find_element(By.NAME, "my-date")
    date_box.clear()
    date_box.send_keys(row["date"])

    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "message"))
    ).text
    print(f"[{i}] {row['name']:<8} -> Form submitted : {message}")
    time.sleep(1)

driver.quit()
print("All forms submitted successfully!")
