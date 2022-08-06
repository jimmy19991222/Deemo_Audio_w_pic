from urllib import error
import requests
import urllib
import time
import sys


def getData(url):
    resp = requests.get(url)
    if resp.status_code >= 300:
        print("HTTP ERROR:", resp.status_code)
        return False
    jsonData = resp.json()
    if "data" not in jsonData:
        print("找不到数据")
        return False
    return resp.json()['data']


def getCidAndTitle(bvid, p=1):
    url = 'https://api.bilibili.com/x/web-interface/view?bvid='+bvid
    data = getData(url)
    print(bvid)
    # print(data)
    if data != False:
        if ('pages' in data):
            title = data['pages'][p-1]['part']
        else:
            title = data['title']
        cid = data['pages'][p-1]['cid']
        return str(cid), title
    else:
        return False, False


def getInformation(bvList):
    infoList = []
    for bvid in bvList:
        item = []
        if len(bvid) < 12:
            print("BVID 格式错误")
            continue
        elif len(bvid) == 12:
            cid, title = getCidAndTitle(bvid)
            if(cid == False):
                continue
            item.append(bvid)
        else:
            cid, title = getCidAndTitle(bvid[:12], int(bvid[13:]))
            if(cid == False):
                continue
            item.append(bvid[:12])
        item.append(cid)
        item.append(title)
        infoList.append(item)

    return infoList


def getAudio(infoList):
    baseUrl = 'http://api.bilibili.com/x/player/playurl?fnval=16&'

    for item in infoList:
        st = time.time()
        bvid, cid, title = item[0], item[1], item[2]
        url = baseUrl+'bvid='+bvid+'&cid='+cid

        audioUrl = requests.get(url).json(
        )['data']['dash']['audio'][0]['baseUrl']

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            # 注意修改referer,必须要加的!
            ('Referer', 'https://api.bilibili.com/x/web-interface/view?bvid='+bvid),
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        if "/" in title:
            title = " ".join(title.split("/"))
        if '\\' in title:
            title = " ".join(title.split("\\"))
        try:
            urllib.request.urlretrieve(
                url=audioUrl, filename='download/'+title+'.mp3')
        except (HTTPError, URLError, ContentTooShortError) as e:
            print("下载失败，因为：", e)
        ed = time.time()
        print(str(round(ed-st, 2))+' seconds download finish:', title)
        time.sleep(1)


if __name__ == '__main__':
    BVList = sys.argv[1:]
    print(f'Downloader Start! {BVList}')
    st = time.time()
    getAudio(getInformation(BVList))
    ed = time.time()
    print('Download Finish All! Time consuming:',
          str(round(ed-st, 2))+' seconds')
