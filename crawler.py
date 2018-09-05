import re
import urllib.error
import time
import urllib.request
import urllib.parse

GBK = 'gbk'
UTF8 = 'utf-8'
novelName = "斗罗大陆"

#匹配小说url
patUrl = '<a cpos="title" href="(.*?)" title="' + novelName + '"'
#匹配每章小说对应的url
pat1 = '<dd><a href="(.*?)">'
#匹配小说内容
pat2 = '<div id="content" class="showtxt">(.*?)</div>'
#匹配小说标题
patTitle = '<h1>(.*?)</h1>'
pat3 = "<[^>]*>|&nbsp;|u3000"

def getUrlData(url, code):
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393")
        request = urllib.request.urlopen(req)
        data = request.read().decode(code, "ignore")
        request.close()
        return data
    except urllib.request.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        time.sleep(3)
    except Exception as e:
        print("exception: " + str(e))
        time.sleep(1)

def changeCode(novelName):
    novelName = novelName.encode("gb2312")
    novelCode = urllib.parse.urlencode({
        "q": novelName
    })
    return novelCode

novelCode = changeCode(novelName)
url = "http://zhannei.baidu.com/cse/search?ie=gbk&s=2758772450457967865&" + str(novelCode)
data = getUrlData(url, UTF8)
novelUnitUrl = re.compile(patUrl, re.S).findall(str(data))[0]
data = getUrlData(novelUnitUrl, UTF8)
novelUrls = re.compile(pat1).findall(data)

for j in range(0, len(novelUrls)):
    novelUrl = "http://www.biqukan.com" + novelUrls[j]
    print(novelUrl)
    novelData = getUrlData(novelUrl, GBK)
    title = re.compile(patTitle).findall(novelData)[0]
    novelData = re.compile(pat2).findall(novelData)
    novelData = str(novelData)
    novelData = novelData.replace('<br /><br />', '\r\n')
    novelData = novelData.replace('&nbsp;&nbsp;&nbsp;&nbsp;', ' ')
    novelData = novelData.replace('u3000', ' ')
    novelData = novelData.replace("\\", '')
    novelData = novelData.replace("['", '')
    novelData = novelData.replace("]", '')
    try:
        file = "D:\studyData\pythonResult" + novelName +".txt"
        fh = open(file, 'a')
        #标题前面只能空两个空格 要不然小说app扫描不出章节
        fh.write('\r\n\r\n  ' + title + '\r\n\r\n')
        fh.write(novelData)
        fh.close()
    except Exception as e:
        print(str(e))