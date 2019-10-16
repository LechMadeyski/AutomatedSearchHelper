#!/usr/bin/env python

"""
Creates proxy file
"""

import argparse
import zipfile
import sys
import configuration
import logging

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "pac_script",
        pacScript : 
            {
                url : "%s"
            }
    };


chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
"""


def create_proxy_configuration(login, password, pac_script, output):
    with zipfile.ZipFile(output, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js % (pac_script, login, password))


def getArgumentsParser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument('--proxy_login', type=str, help='Username for proxy')
    parser.add_argument('--proxy_password', type=str, help='Password for proxy')
    parser.add_argument('--pac_script', default="http://proxy.bg.pwr.wroc.pl/proxy.pac", type=str, help='Pac script')
    parser.add_argument('--output_proxy', default='proxy_auth_plugin.zip', type=str, help='Output file')
    return parser


def main(args=None):
    configuration.configureLogger()
    logger = logging.getLogger('run_articles_download')

    p = getArgumentsParser()
    a = p.parse_args(args=args)

    logger.info("Starting create_proxy_configuration with following arguments")
    logger.info("proxy_login = " + a.proxy_login)
    logger.info("proxy_password = " + a.proxy_password)
    logger.info("output_proxy = " + a.output_proxy)
    logger.info("output_pac_script = " + a.pac_script)

    create_proxy_configuration(a.proxy_login, a.proxy_password, a.pac_script, a.output_proxy)


if __name__ == '__main__': sys.exit(main())
