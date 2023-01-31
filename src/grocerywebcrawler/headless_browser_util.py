import json
from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs

"""
https://www.rkengler.com/how-to-capture-network-traffic-when-scraping-with-selenium-and-python/
https://www.selenium.dev/documentation/webdriver/drivers/

"""


def _get_search_requests(logs):
    network_events = []
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
        ):
            network_events.append(log)
    search_url = "https://www.safeway.com/abs/pub/xapi/search/products"
    search_requests = []
    for network_call in network_events:
        if "params" in network_call:
            params = network_call["params"]
            if "request" in params:
                request = params["request"]
                if "url" in request:
                    if request["url"].startswith(search_url):
                        search_requests.append(network_call)
    return search_requests


def _get_request_id(search_requests):
    if len(search_requests) > 1:
        raise Exception("more than 1 search request")
    else:
        search_request = search_requests[0]
        url = search_request["params"]["request"]["url"]
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        request_id = query_params["request-id"][0]
    return request_id


def headless_browser_request_id() -> int:
    url = "https://www.safeway.com/shop/deals/member-specials.html"
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    options = webdriver.ChromeOptions()
    options.headless = True
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                          desired_capabilities=capabilities, options=options) as driver:
        driver.get(url)
        logs = driver.get_log("performance")
        search_requests = _get_search_requests(logs)
        request_id = _get_request_id(search_requests)
        sleep(3)
        driver.quit()
        print(f"Safeway request id obtained. request_id: {request_id}")
        return request_id
