import os
import time
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class XomeListings:

    def __init__(self, url, site, rough):
        self.rough = rough
        self.site = site
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)

        # Browser options to prevent detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-search-engine-choice-screen')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

        # Spoofing capabilities
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Handling SSL certificates and insecure content
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')

        # Disable password manager prompts
        prefs = {
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False
        }
        options.add_experimental_option('prefs', prefs)

        # Initialize WebDriver
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get(url)
        self.driver.implicitly_wait(30)
        self.wait = WebDriverWait(self.driver, 30)
        self.captcha_wait = WebDriverWait(self.driver, 300)
        self.set_property_filter_to_default()

    def get_search_terms(self):
        with open('search_terms.txt', 'r') as file:
            search_terms = [each_search.strip() for each_search in file.readlines()]
        return search_terms

    def set_property_filter_to_default(self):
        # Click filter button
        click_filter = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="ddbtn-label-filters"]'))
        )
        click_filter.click()

        # Uncheck property type checkboxes
        property_type_box = self.driver.find_element(By.CSS_SELECTOR, '[class="prop-home-type-checkbox"]')

        all_active = property_type_box.find_elements(By.XPATH, "//span[contains(@class, 'active')]")
        if len(all_active) > 0:
            for each_active in all_active:
                each_active.click()

        # Apply filter
        apply_filter = self.driver.find_element(By.CSS_SELECTOR, '[id="desktop-apply"]')
        apply_filter.click()

    def set_filter(self, keyword):

        # Click filter button
        click_filter = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="ddbtn-label-filters"]'))
        )
        click_filter.click()
        print('filter clicked')

        # Input keyword
        keyword_field = self.driver.find_element(By.CSS_SELECTOR, '[id="filters-keyword"]')
        keyword_field.clear()
        keyword_field.send_keys(keyword)
        print('Keyword inserted')

        # Apply filter
        apply_filter = self.driver.find_element(By.CSS_SELECTOR, '[id="desktop-apply"]')
        apply_filter.click()
        print('Filter applied')

    def get_new_url(self):
        all_new_listings = []
        # Get all listing boxes
        all_new = self.driver.find_elements(By.CSS_SELECTOR, '[class="ribbon-new ribbon"]')
        if len(all_new) < 1:
            return
        all_listings = self.driver.find_elements(By.XPATH, "//div[@id='mapsearch-results-body']//div[contains(@class, 'mapsearch-singleprop')]")
        listing_to_scrape = all_listings[:len(all_new)]

        for each_listing in listing_to_scrape:
            url = f"https://www.xome.com{each_listing.get_attribute('data-url')}"
            all_new_listings.append(url)

        return all_new_listings

    def operate(self):
        all_keywords = self.get_search_terms()

        i = 0
        for keyword in all_keywords:
            try:
                i += 1
                print(f'Checking data for {keyword}: {i}')
                self.set_filter(keyword)
                time.sleep(2)
                all_url = self.get_new_url()

                # Check if all_url is not None before iterating
                if all_url:
                    for each_url in all_url:
                        self.save_to_txt(each_url, keyword)
                    print(f'Data for {keyword} saved')
                else:
                    print(f'No new listings found for {keyword}')
                print('\n')
            except Exception as e:
                print(e)
                self.driver.refresh()

    def read_from_txt(self, keyword):
        """Reads the main file to retrieve all previously stored entries."""
        directory = self.site
        os.makedirs(directory, exist_ok=True)  # Ensure directory exists
        file_path = f'{directory}/{keyword}.txt'

        if not os.path.exists(file_path):
            return []

        with open(file_path, 'r') as file:
            search_terms = [each_search.strip() for each_search in file.readlines()]
        return search_terms

    def save_to_txt(self, content, keyword):
        """Saves new listings to both the main file (append) and a new file (write mode)."""
        search_terms = self.read_from_txt(keyword)
        directory = self.site
        os.makedirs(directory, exist_ok=True)  # Ensure directory exists

        if content not in search_terms:
            # Main file (append mode)
            main_file_path = f'{directory}/{keyword}.txt'
            with open(main_file_path, 'a') as main_file:
                main_file.write(f'{content}\n')

            # New file (write mode, overwrite each time with new data)
            new_file_path = f'{directory}/{keyword}_{self.rough}_new.txt'
            with open(new_file_path, 'a') as new_file:
                new_file.write(f'{content}\n')  # Only the latest entry will be written

            print(f"New entry added: {content} to {new_file_path}")

        else:
            print(f"Entry already exists: {content}")

    def close_driver(self):
        time.sleep(20)
        self.driver.quit()


