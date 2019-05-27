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
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: [
            "localhost",
            "https://sdfestaticassets-eu-west-1.sciencedirectassets.com",
            "https://assets.adobedtm.com",
            "https://ars.els-cdn.com",
            "https://cdn.plu.mx",
            "https://w.usabilla.com",
            "https://cdnjs.cloudflare.com",
            "https://www.googletagservices.com",
            "https://dpm.demdex.net"
            ]
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

def create_proxy_configuration(url, port, login, password, output):
    with zipfile.ZipFile(output, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js%(url, port, login, password))

def getArgumentsParser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument('--proxy_url', default='156.17.79.2', type=str, help='Url of proxy')
    parser.add_argument('--proxy_port', default=3128, type=int, help='Port of proxy')
    parser.add_argument('--proxy_login', type=str, help='Username for proxy')
    parser.add_argument('--proxy_password', type=str, help='Password for proxy')
    parser.add_argument('--output_proxy', default='proxy_auth_plugin.zip', type=str, help='Output file')
    return parser

def main(args = None):
    configuration.configureLogger()
    logger = logging.getLogger('run_articles_download')

    p = getArgumentsParser();
    a = p.parse_args(args=args)

    logger.info("Starting create_proxy_configuration with following arguments")
    logger.info("proxy_url = " + a.proxy_url)
    logger.info("proxy_port = " + str(a.proxy_port))
    logger.info("proxy_login = " + a.proxy_login)
    logger.info("proxy_password = " + a.proxy_password)
    logger.info("output_proxy = " + a.output_proxy)

    create_proxy_configuration(a.proxy_url, a.proxy_port, a.proxy_login, a.proxy_password, a.output_proxy)

if __name__ == '__main__': sys.exit(main())
