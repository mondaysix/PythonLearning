from selenium import webdriver

import unittest,time

class new_sub_count(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.jianshu.com/p/c85f5b6c6144"
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_refresh_count(self):
        driver = self.driver
        driver.get(self.base_url)#启动浏览器
        for i in range(100):
            time.sleep(2)
            driver.refresh()
        driver.quit()


if __name__ == '__main__':
        unittest.main()