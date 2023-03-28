import random
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class ProxyLine:
    number: int
    ip: str
    port: str
    type: str
    country: str
    speed: str
    last: str

    def __init__(self, number, ip, port, type, country, speed, last):
        self.number = number
        self.ip = ip
        self.port = port
        self.type = type
        self.country = country
        self.speed = speed
        self.last = last


class ProxyUtil:
    __all_proxies = None
    __proxies_with_failure_count = None
    __previous = None
    proxy_url = "https://www.proxy-list.download/api/v1/get?type=https&country=US"

    proxy_url2 = "https://advanced.name/freeproxy?country=US&type=https"

    @staticmethod
    def init_proxies2():
        url = ProxyUtil.proxy_url2
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.headless = True
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                  desired_capabilities=capabilities, options=options)
        driver.get(url)
        table_rows = driver.find_element(by="xpath",
                                         value="/html/body/section[2]/div[4]/table/tbody").text.splitlines()
        all_proxies_from_advanced = []
        for row in table_rows:
            splitBySpaces = row.split(" ")
            try:
                indexUtilSplitBySpaceUS = 0
                for split in enumerate(splitBySpaces):
                    if split[1] == "US":
                        indexUtilSplitBySpaceUS = split[0]
                proxyLine = ProxyLine(splitBySpaces[0], splitBySpaces[1], splitBySpaces[2], splitBySpaces[3],
                                      splitBySpaces[indexUtilSplitBySpaceUS],
                                      int(splitBySpaces[indexUtilSplitBySpaceUS + 1]),
                                      splitBySpaces[indexUtilSplitBySpaceUS + 2])
                all_proxies_from_advanced.append(proxyLine)
            except Exception:
                print("unable to parse proxy list")
        all_proxies_from_advanced = sorted(all_proxies_from_advanced, key=lambda x: x.speed)

        ProxyUtil.__all_proxies = []
        ProxyUtil.__proxies_with_failure_count = {}
        for proxy in all_proxies_from_advanced:
            if f"{proxy.ip}:{proxy.port}" not in ProxyUtil.__all_proxies:
                ProxyUtil.__all_proxies.append(f"{proxy.ip}:{proxy.port}")
                ProxyUtil.__proxies_with_failure_count[f"{proxy.ip}:{proxy.port}"] = 0

    @staticmethod
    def getProxy():
        if ProxyUtil.getAllProxies() == None:
            ProxyUtil.init_proxies2()

        if ProxyUtil.getPrevious() != None:
            return {"https": ProxyUtil.__previous}

        smallestFailureCount = float('inf')
        for key in ProxyUtil.getAllProxyFailureCount().keys():
            failureCount = ProxyUtil.getFailureCount(key)
            if failureCount < smallestFailureCount:
                smallestFailureCount = failureCount

        keys_with_smallest = []
        for key in ProxyUtil.getAllProxyFailureCount().keys():
            if ProxyUtil.getFailureCount(key) == smallestFailureCount:
                keys_with_smallest.append(key)

        ProxyUtil.__previous = random.choice(keys_with_smallest)
        return {"https": ProxyUtil.__previous}

    @staticmethod
    def increment(proxy):
        proxyAddress = proxy["https"]
        ProxyUtil.__proxies_with_failure_count[proxyAddress] += 1
        ProxyUtil.__previous = None

    @staticmethod
    def getFailureCount(proxy):
        return ProxyUtil.__proxies_with_failure_count[proxy]

    @staticmethod
    def getAllProxyFailureCount():
        return ProxyUtil.__proxies_with_failure_count;

    @staticmethod
    def getPrevious():
        return ProxyUtil.__previous

    @staticmethod
    def getAllProxies():
        return ProxyUtil.__all_proxies
