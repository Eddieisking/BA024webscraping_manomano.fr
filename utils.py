"""
# Project:
# Author: Eddie
# Date: 
"""
import json

from selenium import webdriver

def create_chrome_driver(*, headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
    )
    return browser

def add_cookies(browser, cookies_file):
    with open(cookies_file, 'r') as file:
        cookies_list = json.load(file)
        for cookies_dict in cookies_list:
            if cookies_dict['secure']:
                browser.add_cookie(cookies_dict)
    return browser
