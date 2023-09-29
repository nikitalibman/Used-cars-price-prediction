

def sel_pars():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&page=1&search_id=7ka6orz363&sort=standard&source=listpage_pagination&ustate=N%2CU'
    chrome_options = Options()


    def extra_arguments(arg):
        chrome_options.add_argument(arg)
        return chrome_options


    extra_arguments('--incognito') # Run Chrome in incognito mode
    extra_arguments('--headless')  # Run Chrome without opening the browser')
    extra_arguments('--blink-settings=imagesEnabled=false')  # Disable images
    extra_arguments('--disable-gpu')  # Disable CSS
    extra_arguments('--disable-software-rasterizer')  # Disable CSS
    extra_arguments('--disable-dev-shm-usage')  # Disable CSS

    chrome_driver = webdriver.Chrome(options=chrome_options)

    # Set Chrome preferences to automatically accept cookies
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    # Get the page content
    chrome_driver.get(url)


    def cookies_accept():
        try:
            # Wait for the consent popup to appear
            consent_popup = WebDriverWait(chrome_driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_consent-popup_1i5cd_1'))
            )
            # Check if the "Accept All" button is present
            accept_all_button = consent_popup.find_element(By.XPATH, '//button[@class="_consent-accept_1i5cd_111"]')
            if accept_all_button.is_displayed():
                # Click the "Accept All" button
                accept_all_button.click()

                # Wait for the consent popup to disappear (short timeout)
                WebDriverWait(chrome_driver, 1).until_not(
                    EC.presence_of_element_located((By.CLASS_NAME, '_consent-popup_1i5cd_1'))
                )
        except:
            pass


    cookies_accept()

    # Find and click the button 'Show more vehicles'
    link = chrome_driver.find_element(By.LINK_TEXT, '+ Show more vehicles')
    link.click()

    cookies_accept()

    cur_url = chrome_driver.current_url

    # Close the WebDriver to properly clean up resources
    chrome_driver.quit()

    return cur_url


if __name__ == "__main__":
    cur_url = sel_pars()
