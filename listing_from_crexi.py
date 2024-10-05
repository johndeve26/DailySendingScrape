import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class CrexiListings:

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
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        # Spoofing capabilities
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Initialize WebDriver
        # self.driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get(url)
        self.driver.implicitly_wait(30)
        self.wait = WebDriverWait(self.driver, 30)

    def get_search_terms(self):
        with open('search_terms.txt', 'r') as file:
            return [each_search.strip() for each_search in file.readlines()]

    def get_listings(self):
        all_listing_url = []
        all_listings = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@data-cy="propertyTile"]//a'))
        )

        for each_listing in all_listings:
            all_listing_url.append(each_listing.get_attribute('href'))

        return all_listing_url

    def operate(self):
        all_keywords = self.get_search_terms()
        for i, keyword in enumerate(all_keywords, start=1):
            try:
                print(f'Checking data for {keyword}: {i}')
                self.driver.get(f'https://www.crexi.com/properties?sort=New%20Listings&showMap=false&term={keyword}')
                all_url = self.get_listings()

                if all_url:
                    for each_url in all_url:
                        self.save_to_txt(each_url, keyword)
                    print(f'Data for {keyword} saved')
                else:
                    print(f'No new listings found for {keyword}')
                print('\n')
            except Exception as e:
                print(e)

    def read_from_txt(self, keyword):
        directory = self.site
        os.makedirs(directory, exist_ok=True)  # Ensure directory exists
        file_path = f'{directory}/{keyword}.txt'

        if not os.path.exists(file_path):
            return []

        with open(file_path, 'r') as file:
            return [each_search.strip() for each_search in file.readlines()]

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
