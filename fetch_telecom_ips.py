from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

URL = "https://api.uouin.com/cloudflare.html"
OUTPUT_FILE = "china_telecom_ips.txt"

def fetch_telecom_ips():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    print("🌐 正在打开网页...")
    driver.get(URL)
    time.sleep(3)  # 等待页面加载完成

    print("⏳ 页面加载完毕，开始解析...")
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    ips = []
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 2:
            line_type = cols[0].get_text(strip=True)
            ip_addr = cols[1].get_text(strip=True)
            if line_type == "电信" and ip_addr:
                ips.append(ip_addr)

    ips = sorted(set(ips))

    if not ips:
        print("⚠️ 未提取到任何电信 IP，可能页面加载失败")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(ips))

    print(f"✅ 共提取 {len(ips)} 个电信 IP，已写入 {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_telecom_ips()
