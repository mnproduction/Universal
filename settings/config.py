# settings/config.py

import os
from pathlib import Path

from selenium.webdriver.chrome.options import Options

class Config:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.model_used = "gpt-4o-mini"

        self.DEBUG_STATE_CONSOLE = True
        self.DEBUG_STATE_FILE = False

class ModelConfig:
    def __init__(self, data: str):
        self.system_message = """You are an intelligent text extraction and conversion assistant. Your task is to extract structured information 
                        from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text, 
                        with no additional commentary, explanations, or extraneous information. 
                        You could encounter cases where you can't find the data of the fields you have to extract or the data will be in a foreign language.
                        Please process the following text and provide the output in pure JSON format with no words before or after the JSON:"""
        self.user_message = f"""Extract the following information from the provided text:\nPage content:\n\n{data}"""

class SeleniumConfig:
    def __init__(self):
        self.DRIVER_PATH = "./webdriver/chromedriver.exe"
        self.SELENIUM_FOLDER = str(Path.joinpath(Path(__file__).parent.parent, 'crawler', 'data', 'selenium'))
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.OPTIONS = Options()
        self.OPTIONS.add_argument("--window-size=1920,1080")
        self.OPTIONS.add_argument(f"--user-data-dir={self.SELENIUM_FOLDER}")
        self.OPTIONS.add_argument("--disable-blink-features=AutomationControlled")
        self.OPTIONS.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.OPTIONS.add_experimental_option("useAutomationExtension", False)
        self.OPTIONS.add_argument("--disable-gpu")
        self.OPTIONS.add_argument("--disable-dev-shm-usage")
        self.OPTIONS.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

class Pricing:
    def __init__(self):
        self.gpt_4o_mini = {
            "input": 0.150 / 1_000_000,
            "output": 0.600 / 1_000_000
        }
        self.gpt_4o = {
            "input": 2.5 / 1_000_000,
            "output": 10 / 1_000_000
        }

config = Config()

selenium_config = SeleniumConfig()

pricing = Pricing()


# Настройки для stealth
# STEALTH_SETTINGS = {
#     'languages': ['en-US', 'en'],
#     'vendor': 'Google Inc.',
#     'platform': 'Win32',
#     'webgl_vendor': 'Google Inc. (NVIDIA)',
#     'renderer': 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Ti (0x00001B06) Direct3D11 vs_5_0 ps_5_0, D3D11)',
#     'fix_hairline': True
# }

# SERVICE_SETTINGS = {'executable_path': DRIVER_PATH}