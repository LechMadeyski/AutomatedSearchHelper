import os
import zipfile

from selenium import webdriver

# PROXY_HOST = '156.17.79.2'  # rotating proxy or host
# PROXY_PORT = 3128 # port
# PROXY_USER = L # username
# PROXY_PASS = P # password


# manifest_json = """
# {
#     "version": "1.0.0",
#     "manifest_version": 2,
#     "name": "Chrome Proxy",
#     "permissions": [
#         "proxy",
#         "tabs",
#         "unlimitedStorage",
#         "storage",
#         "<all_urls>",
#         "webRequest",
#         "webRequestBlocking"
#     ],
#     "background": {
#         "scripts": ["background.js"]
#     },
#     "minimum_chrome_version":"22.0.0"
# }
# """

# background_js = """
# var config = {
#         mode: "fixed_servers",
#         rules: {
#         singleProxy: {
#             scheme: "http",
#             host: "%s",
#             port: parseInt(%s)
#         },
#         bypassList: [
#             "localhost",
#             "https://sdfestaticassets-eu-west-1.sciencedirectassets.com",
#             "https://assets.adobedtm.com",
#             "https://ars.els-cdn.com",
#             "https://cdn.plu.mx",
#             "https://w.usabilla.com",
#             "https://cdnjs.cloudflare.com",
#             "https://www.googletagservices.com",
#             "https://dpm.demdex.net"
#             ]
#         }
#     };

# chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

# function callbackFn(details) {
#     return {
#         authCredentials: {
#             username: "%s",
#             password: "%s"
#         }
#     };
# }

# chrome.webRequest.onAuthRequired.addListener(
#             callbackFn,
#             {urls: ["<all_urls>"]},
#             ['blocking']
# );
# """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


# def getDriver(proxyFile=None):
#     path = os.path.dirname(os.path.abspath(__file__))
#     chrome_options = webdriver.ChromeOptions()
#     if use_proxy:
#         pluginfile = 'proxy_auth_plugin.zip'

#         with zipfile.ZipFile(pluginfile, 'w') as zp:
#             zp.writestr("manifest.json", manifest_json)
#             zp.writestr("background.js", background_js)
#         chrome_options.add_extension(pluginfile)
#     if user_agent:
#         chrome_options.add_argument('--user-agent=%s' % user_agent)
#     driver = webdriver.Chrome(
# #        os.path.join(path, 'chromedriver'),
#         chrome_options=chrome_options)
#     return driver


def getDriver(proxyFile=None):
    chrome_options = webdriver.ChromeOptions()
    if proxyFile is not None:
        pluginfile = proxyFile
        chrome_options.add_extension(pluginfile)

    preferences = {
                   "download.default_directory": os.getcwd(),
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True}
    chrome_options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(
        chrome_options=chrome_options)
    driver.refresh()

    return driver
