# crawler/selenium_crawler.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from settings.config import selenium_config
from utils.logger import Logger

logger = Logger(__name__)


class SeleniumCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(selenium_config.DRIVER_PATH), options=selenium_config.OPTIONS)

    def wait_for_page_load(self, timeout: int = 30):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except Exception as e:
            logger.error(f"Error waiting for page load: {e}")
            return False
        return True

    def scroll_page(self, pages_to_scroll: int = 1):
        for _ in range(pages_to_scroll):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.wait_for_page_load()

    def get_html(self, url: str, pages_to_scroll: int = 0) -> str:
        try: 
            self.driver.get(url)
            self.wait_for_page_load()
            self.scroll_page(pages_to_scroll=pages_to_scroll)
            html = self.driver.page_source
            return html
        except Exception as e:
            logger.error(f"Error fetching HTML: {e}")
            return ""
        finally:
            self.driver.quit()

