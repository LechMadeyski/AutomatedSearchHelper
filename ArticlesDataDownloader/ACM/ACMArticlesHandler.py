
import selenium
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

class ACMArticlesHandler():
    def __init__(self, driver):
        self.driver = driver

    def getArticle(self, url):
        logging.error("ACM HANDLER IS NOT IMPLEMENTED YET " + url + " will not be handled")
        return None

    def linkPart(self):
        return "dl.acm.org"

    def name(self):
        return "ACM"

