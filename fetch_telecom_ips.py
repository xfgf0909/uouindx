from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

URL = "https://api.uouin.com/cloudflare.html"
OUTPUT_FILE = "china_telecom_ips.txt"

def fetch_telecom_ips():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    time.sleep(3)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    ips = []
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 2 and cols[0].get_text(strip=True) == "电信":
            ips.append(cols[1].get_text(strip=True))
    ips = sorted(set(ips))
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(ips))
    print(f"✅ 提取完成，共 {len(ips)} 个电信 IP。")

if __name__ == "__main__":
    fetch_telecom_ips()
