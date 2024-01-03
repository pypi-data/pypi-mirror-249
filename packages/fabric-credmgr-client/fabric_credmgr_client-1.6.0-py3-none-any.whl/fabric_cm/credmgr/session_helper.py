import logging
import time
from typing import List

from selenium import webdriver


class SessionHelper:
    def __init__(self, *, url: str = "https://cm.fabric-testbed.net", cookie_name: str = "fabric-service",
                 wait_timeout: int = 500, wait_interval: int = 5):
        self.logger = logging.getLogger()
        self.url = url
        self.cookie_name = cookie_name
        self.wait_timeout = wait_timeout
        self.wait_interval = wait_interval

    def __extract_fabric_cookie(self, *, cookies: List[dict]):
        ret_val = None
        for c in cookies:
            name = c.get('name')
            if ret_val is None and name == self.cookie_name:
                ret_val = c.get('value')
                ret_val = f"{name}={ret_val}"
                break
        self.logger.debug(f"Returning cookie: {ret_val}")
        return ret_val

    def login(self, browser_name: str = "chrome"):
        if browser_name.lower() == "firefox":
            browser = webdriver.Firefox()
        elif browser_name.lower() == "safari":
            browser = webdriver.Safari()
        elif browser_name.lower() == "edge":
            browser = webdriver.Edge()
        else:
            browser = webdriver.Chrome()
        browser.get(self.url)

        # Get the cookies
        cookie = self.__extract_fabric_cookie(cookies=browser.get_cookies())
        start = time.time()
        while cookie is None or time.time() > start + self.wait_timeout:
            time.sleep(self.wait_interval)
            self.logger.info("Checking if the user has logged in!")
            cookie = self.__extract_fabric_cookie(cookies=browser.get_cookies())

        # Print the cookies
        if cookie is None:
            msg = f"Timeout occurred - User did not login within {self.wait_timeout} or {self.cookie_name} not found"
            self.logger.error(msg)
            raise Exception(msg)

        # Close the browser
        browser.quit()

        #return requests.cookies.create_cookie(name=self.cookie_name, value=cookie)
        return cookie
