import httpx

client = httpx.Client()
response = client.get("https://wallhaven.cc/api/v1/search")

# json 转 字典
pictures = response.json()
# print(pictures["data"])
data = pictures["data"]
pictures = []
class picture:
    def __init__(self,id,url,dimension_x,dimension_y):
        self.id = id
        self.url = url
        self.dimension_x = dimension_x
        self.dimension_y = dimension_y

for item in data:
    temp = []
    temp.append(item["id"])
    temp.append(item["url"])
    temp.append(item["dimension_x"])
    temp.append(item["dimension_y"])
    pictures.append(temp)
    # print("----"*10)
print(pictures)

