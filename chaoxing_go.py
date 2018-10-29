import requests
import json
import re
import time
import hashlib


class chaoxing:
    def __init__(self, cookie):
        self.headers = {'Cookie': cookie,
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

    def load(self):
        # 获得所有课程数据
        html_课程 = requests.get(url="http://mooc1-1.chaoxing.com/visit/courses", headers=self.headers).text
        pattern_课程 = re.compile('<h3 class="clearfix" >.*?\'(.*?)\'', re.S)
        cap_课程 = re.findall(pattern_课程, html_课程)
        self.list = []
        print("*" * 20 + "清单" + "*" * 20)
        times = 0
        for i in cap_课程:
            url = "http://mooc1-1.chaoxing.com" + i
            html_课程列 = requests.get(url=url, headers=self.headers).text
            pattern_课程列 = re.compile(
                '<span class="articlename">.*?chapterId=(.*?)&courseId=(.*?)&clazzid=(.*?)&enc=(.*?)\'.*?title="(.*?)"',
                re.S)
            cap_课程列 = re.findall(pattern_课程列, html_课程列)
            for m in cap_课程列:
                self.list.append({"chapterId": m[0], "courseId": m[1], "clazzid": m[2], "enc": m[3], "title": m[4]})
                print(str(times) + m[4])
                times = times + 1
        print("*" * 20 + "结束" + "*" * 20)

    def study(self, index):
        # xxx
        list = self.list[index]
        json_mArg = json.loads("{}")
        for i in range(0, 4):
            if (i == 3):
                print("无需学习")
                return
            print("检测页面：" + str(i))
            html_1 = requests.get(
                url="http://mooc1-1.chaoxing.com/knowledge/cards?clazzid=%s&courseid=%s&knowledgeid=%s&num=%d&v=20160407-1" % (
                    list['clazzid'], list['courseId'], list['chapterId'], i), headers=self.headers).text
            pattern_1 = re.compile('mArg = {(.*?)};', re.S)
            cap_1 = re.search(pattern_1, html_1)
            try:
                json_mArg = json.loads("{%s}" % (cap_1.group(1)))
            except:
                continue
            if (len(json_mArg["attachments"]) > 0 and "name" in json_mArg["attachments"][0][
                "property"].keys()):
                if ("isPassed" in json_mArg["attachments"][0].keys() and json_mArg["attachments"][0][
                    "isPassed"] == True):
                    print("已经学习过")
                    return
                else:
                    break
            else:
                continue
        html_2 = requests.get(url="https://mooc1-1.chaoxing.com/ananas/status/%s?k=%s&_dc=%d" % (
            json_mArg['attachments'][0]['objectId'], json_mArg['defaults']['fid'],
            int(round(time.time() * 1000))), headers=self.headers).text
        json_info = json.loads(html_2)
        html_3 = requests.get(
            url="https://mooc1-1.chaoxing.com/multimedia/log/%s?objectId=%s&otherInfo=%s&clipTime=0_%s&rt=0.9&clazzId=%s&dtype=Video&duration=%s&jobid=%s&userid=%s&view=pc&playingTime=%s&isdrag=3&enc=%s" % (
                json_info['dtoken'], json_info['objectid'], json_mArg['attachments'][0]['otherInfo'],
                json_info['duration'], list['clazzid'],
                json_info['duration'], json_mArg['attachments'][0]['jobid'], json_mArg['defaults']['userid'],
                json_info['duration'],
                self.getEnc(list['clazzid'], json_mArg['defaults']['userid'], json_mArg['attachments'][0]['jobid'],
                            json_info['objectid'], json_info['duration'], json_info['duration'])),
            headers=self.headers).text
        json_pass = json.loads(html_3)
        if (json_pass["isPassed"] == True):
            print("学习成功")
        else:
            print("学习失败")

    def getEnc(self, clazzId, userid, jobid, objectId, duration, clipTime):
        loc4 = duration
        text = "[%s][%s][%s][%s][%s][d_yHJ!$pdA~5][%s][0_%s]" % (
            clazzId, userid, jobid, objectId, str(int(loc4) * 1000), str(int(duration) * 1000), clipTime)
        hash = hashlib.md5()
        hash.update(text.encode(encoding='utf-8'))
        return hash.hexdigest()


cx = chaoxing("cookie")
cx.load()
while True:
    print("请输入要完成的编号：")
    text = input()
    if (text == "q"):
        break
    cx.study(int(text))

#for i in range(0,135):
#    cx.study(i)
#    time.sleep(60)
