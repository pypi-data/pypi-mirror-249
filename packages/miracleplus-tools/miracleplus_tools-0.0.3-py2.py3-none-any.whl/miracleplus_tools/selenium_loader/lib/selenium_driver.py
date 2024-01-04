import os
from selenium.webdriver import Chrome, Remote
from selenium.webdriver.chrome.options import Options

class SeleniumDriver:

    @classmethod
    def init_driver(cls) -> Remote:
        options = Options()
        proxy = os.environ.get("SELENIUM_PROXY", None)
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.146 Safari/537.36")

        remote_webdriver = os.getenv("REMOTE_SELENIUM_URL", None)
        if remote_webdriver:
            options.add_argument(r"--user-data-dir=/home/seluser/.config/google-chrome")
            options.add_argument(r'--profile-directory=ublock')
            return Remote(command_executor=remote_webdriver, options=options)
        options.binary_location =os.environ.get("SELENIUM_LOCATION", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        return Chrome(options=options)
