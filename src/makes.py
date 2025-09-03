"""
This module scraps all marks names and save it into a list.
"""
from decline_cookies import get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


#chrome_driver.get_screenshot_as_file('screenshot.png')  # Take a screenshot
csv_path = "src/makes_list.csv"

def all_makes(url):
    chrome_driver, _ = get_url(url)
    # Wait for the select-make-container to be present
    make_container = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "hf-tabs__content"))
    )
    # Find the button with all the makes inside the container and click it
    makes_button = make_container.find_element(By.CLASS_NAME, "hf-searchmask-form__filter__make")
    # chrome_driver.execute_script("arguments[0].scrollIntoView(true);", makes_button)
    makes_button.click()

    wait = WebDriverWait(chrome_driver, 10)
    makes_button = wait.until(EC.presence_of_all_elements_located((By.ID, 'make')))

    makes_list = []

    for make in makes_button:
        makes_list.append(make.text)

    # filter the makes list
    makes_list = makes_list[0].strip().split('\n')[1:-1]

    chrome_driver.quit()

    return makes_list


def save_makes_to_file(url):
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        for make in all_makes(url):
            writer.writerow([make])


if __name__ == "__main__":
    url = 'https://www.autoscout24.com/'
    csv_path = "src/makes_list.csv"
    makes = save_makes_to_file(url)
    print(f"Saved makes to '{csv_path}'")
