import os

from selenium import webdriver

from ArticlesDataDownloader.download_utilities import clear_download_directory, DOWNLOAD_DIRECTORY


def getDriver(proxyFile=None):
    chrome_options = webdriver.ChromeOptions()
    if proxyFile:
        pluginfile = proxyFile
        chrome_options.add_extension(pluginfile)

    clear_download_directory()

    preferences = {
                   "download.default_directory": DOWNLOAD_DIRECTORY,
                   "directory_upgrade": True,
                   "plugins.always_open_pdf_externally": True,
                   "safebrowsing.enabled": True}

    chrome_options.add_experimental_option("prefs", preferences)
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--kiosk")

    driver = webdriver.Chrome(
        options=chrome_options)
    driver.refresh()

    return driver
