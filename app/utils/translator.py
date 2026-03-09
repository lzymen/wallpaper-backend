# app/utils/translator.py
import random
import hashlib
import httpx
from app.core.config import settings


async def translate_zh_to_en(query: str) -> str:
    """
    使用百度翻译 API 将中文关键词转为英文
    """
    if not query:
        return ""

    # 从 settings 中读取环境变量
    appid = settings.BAIDU_APPID
    appkey = settings.BAIDU_APPKEY

    endpoint = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    salt = str(random.randint(32768, 65536))

    # 按照百度文档要求生成签名
    sign_str = appid + query + salt + appkey
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    payload = {
        'appid': appid,
        'q': query,
        'from': 'zh',
        'to': 'en',
        'salt': salt,
        'sign': sign
    }

    async with httpx.AsyncClient() as client:
        try:
            # 发送请求
            r = await client.post(endpoint, data=payload, timeout=10.0)
            result = r.json()

            # 提取翻译结果
            if "trans_result" in result:
                return result["trans_result"][0]["dst"]
            return query  # 翻译失败则返回原词保底
        except Exception as e:
            print(f"❌ 翻译服务异常: {e}")
            return query


if __name__ == '__main__':
    import asyncio

    # 在异步环境中运行
    en = asyncio.run(translate_zh_to_en("七龙珠"))
    print(en)