import requests
from bs4 import BeautifulSoup

URL = "https://api.uouin.com/cloudflare.html"
OUTPUT_FILE = "china_telecom_ips.txt"

def fetch_telecom_ips():
    try:
        # 请求网页
        res = requests.get(URL, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        res.encoding = res.apparent_encoding
    except Exception as e:
        print("❌ 请求网页失败：", e)
        return

    soup = BeautifulSoup(res.text, "html.parser")

    ips = []
    # 遍历表格的每一行
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 2:
            line_type = cols[0].get_text(strip=True)
            ip_addr = cols[1].get_text(strip=True)
            if line_type == "电信" and ip_addr:
                ips.append(ip_addr)

    ips = sorted(set(ips))  # 去重并排序

    if not ips:
        print("⚠️ 未提取到任何电信 IP，网页结构可能变化。")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(ips))

    print(f"✅ 共提取 {len(ips)} 个电信 IP：")
    for ip in ips:
        print(ip)

if __name__ == "__main__":
    fetch_telecom_ips()
