import httpx

# 1. 发送 GET 请求给百度
# 注意：有些网站会拦截没有“身份标识”的请求，所以最好带上 headers 伪装成浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = httpx.get("https://www.baidu.com", headers=headers)

# 2. 打印状态码 (200 表示成功)
print(f"状态码: {response.status_code}")

# 3. 打印网页标题 (简单提取一下)
# response.text 是整个网页的 HTML 源码，非常长
html_content = response.text
print(html_content)
# if "<title>" in html_content:
#     title_start = html_content.find("<title>") + len("<title>")
#     title_end = html_content.find("</title>")
#     print(f"网页标题: {html_content[title_start:title_end]}")

# 4. 如果你想看源码的