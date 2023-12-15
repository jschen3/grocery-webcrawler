import json
import sys
from time import sleep
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

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
    if len(search_requests)!=1:
        return None
    else:
        search_request = search_requests[0]
        ocp_key = search_requests[0]["params"]["request"]["headers"]["Ocp-Apim-Subscription-Key"]
        # print(search_requests[0]["params"]["request"]["headers"])
        url = search_request["params"]["request"]["url"]
        # print(url)
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        request_id = query_params["request-id"][0]
        # print(query_params)
    return {
        "request-id": request_id,
        "ocp-apim-subscription-key": ocp_key}


def headless_browser_request_id() -> dict:

    url = "https://www.safeway.com/shop/deals/member-specials.html"
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")
    options.headless = True
    sys.path.insert(0, '/opt/google/chrome')
    driver = webdriver.Chrome(options=options)
    attempts=0
    while attempts<3:
        driver.get(url)
        logs = driver.get_log("performance")
        search_requests = _get_search_requests(logs)
        request_id = _get_request_id(search_requests)
        if request_id!=None:
            driver.quit()
            return request_id
        sleep(3)
    raise Exception("unable to get request id in 3 tries.")
    # print(f"Safeway request id obtained. request_id: {request_id}")

