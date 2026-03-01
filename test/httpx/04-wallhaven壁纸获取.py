import httpx

# 1. 你的局域网 IP
IP = "192.168.28.140"
# 2. 准备测试一个谷歌的图片（或者任意一张图片链接）
test_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"


def test_my_backend():
    print(f"🚀 开始测试后端代理...")
    proxy_api = f"http://{IP}:8000/api/v1/wallpapers/proxy?url={test_url}"

    try:
        resp = httpx.get(proxy_api, timeout=10.0)
        if resp.status_code == 200:
            print(f"✅ 成功！后端已正确转发图片。内容大小: {len(resp.content)} 字节")
        elif resp.status_code == 404:
            print(f"❌ 失败：后端返回 404。说明你的接口路径 /api/v1/wallpapers/proxy 还是没挂载成功。")
        else:
            print(f"⚠️ 状态码 {resp.status_code}：后端通了，但请求原始图片失败。请检查你电脑的 Clash 代理。")
    except Exception as e:
        print(f"🔥 连不上后端：{e}。请检查 main.py 是否在运行，且 host 是否为 0.0.0.0")


if __name__ == "__main__":
    test_my_backend()