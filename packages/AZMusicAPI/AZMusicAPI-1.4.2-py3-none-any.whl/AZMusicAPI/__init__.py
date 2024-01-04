import requests


# AZ Studio版权所有
# 该项目仅供娱乐 请勿用于违法事业 违者与AZ Studio无关

def getmusic(keyword, api, number=20):
    number = int(number)
    # 获得指定关键词的歌曲 关键词可为 歌手/歌曲名/专辑名
    # keyword：关键词 number:返回歌曲数量,可选,默认20 api:自行部署neteasecloudmusicapi的地址
    # 返回值说明：正常返回列表  "Error 0"：没有结果 "Error 1":用户未输入
    search_url = api + "search"
    search_data = {"keywords":keyword}
    if len(keyword) > 0:
        try:
            response_data = requests.get(search_url, params=search_data,  timeout=20).json()
        except:
            return "NetworkError"
        songs_data = response_data['result']['songs']
        if len(response_data['result']['songs']) <= 0:
            return "Error 0"
        else:
            data = []
            try:
                for i in range(len(songs_data)):
                    artists = ""
                    for y in range(len(songs_data[i]["artists"])):
                        if y != 0:
                            artists = artists + ","
                        artists = artists + songs_data[i]["artists"][y]["name"]
                    data.append({"id": songs_data[i]['id'], "name": songs_data[i]['name'],"artists": artists, "album": songs_data[i]['album']["name"]})
            except:
                data.append({"id": '-1', "name": 'error', "artists": 'error',
                             "album": 'error'})
            if len(data) > number:
                data = data[:number]
            return data
    else:
        return "Error 1"


def geturl(id,api):
    # 获取音乐的音频地址
    # id:歌曲的id值  api:自行部署neteasecloudmusicapi的地址
    # 返回值：正常:返回音频链接  "Error 3":id不正确或无版权
    search_url = api + "song/url"
    search_data = {"id": id}
    try:
        response_data = requests.get(search_url, params=search_data).json()
    except:
        return "NetworkError"
    try:
        song_url = response_data['data'][0]["url"]
    except:
        return "Error 3"
    return song_url





u = input("请输入您需要的歌曲名称：")
data = getmusic(u,"https://ncma.zenglingkun.cn/",number=5)
print(geturl(data[0]["id"],"https://ncma.zenglingkun.cn/"))

