
import httpx
import time

start_time = time.time()

# 方式1：3次请求 = 创建3次连接（慢）
httpx.get("https://wallhaven.cc/api/v1/search")
httpx.get("https://wallhaven.cc/api/v1/search")
httpx.get("https://wallhaven.cc/api/v1/search")
end_time = time.time()
duration = end_time - start_time

start_time1 = time.time()
# 方式2：3次请求 = 只用1个连接（快）
# 同步（一个一个等）
with httpx.Client() as client:
    client.get("https://wallhaven.cc/api/v1/search")
    client.get("https://wallhaven.cc/api/v1/search")
    client.get("https://wallhaven.cc/api/v1/search")

end_time1 = time.time()
duration2 = end_time1 - start_time1

print(duration)
print(duration2)

# 异步（同时发）
import asyncio
# async with 必须在 async 函数 里使用

import httpx
import asyncio

start_time2 = time.time()
async def main():  # ✅ 必须包在 async def 里
    async with httpx.AsyncClient() as client:
        r1, r2, r3 = await asyncio.gather(
            client.get("https://wallhaven.cc/api/v1/search"),
            client.get("https://wallhaven.cc/api/v1/search"),
            client.get("https://wallhaven.cc/api/v1/search")
        )
        print(r1.status_code, r2.status_code, r3.status_code)

# 运行
asyncio.run(main())

end_time2 = time.time()
duration3 = end_time2- start_time2
print(duration3)