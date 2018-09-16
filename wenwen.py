# coding:utf-8
import urllib.request
import urllib
import re
from bs4 import BeautifulSoup
import codecs
import sys
import json




'''
从搜狗问问爬取每个分类标签下的问题答案集，每个问题追加为json格式：
{
    "answer": [
        "我一直用的是云末感觉还是挺稳定的。"
    ],
    "tag": {
        "75023": "英雄联盟"
    },
    "question": "网易uu加速器加速lol怎么样",
    "hasAnswer": true
}
'''
global rootUrl

headers = {
}
# 加载页面内容
def LoadPage(url):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'

        headers = {"User-Agent": user_agent}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        html = response.read()
        allTitles = []
        allTitles = GetTitle(html)
        if allTitles:
            QuestionAnswers = []
            QuestionAnswers = GetQuestionAnswers(allTitles)
            if QuestionAnswers:
                return QuestionAnswers
    except Exception as e:
        print(str(e))


# 获取问题标题
def GetTitle(html):
    allTitles = []
    myAttrs = {'class': 'sort-lst-tab'}
    bs = BeautifulSoup(html)
    titles = bs.find_all(name='a', attrs=myAttrs)
    for titleInfo in titles:
        item = {}
        titleInfoStr = str(titleInfo)
        questionInfo = re.findall(r'sort-tit">(.*?)</p>', titleInfoStr, re.S)
        question = questionInfo[0]
        answerInfo = re.findall(r'sort-rgt-txt">(.*?)</span>', titleInfoStr, re.S)
        if u'0个回答' in answerInfo:
            item['hasAnswer'] = False
        else:
            item['hasAnswer'] = True
        tags = re.findall(r'sort-tag" data-id=(.*?)/span>', titleInfoStr, re.S)
        tagInfo = {}
        for tag in tags:
            tagId = re.findall(r'"(.*?)">', tag, re.S)
            tagName = re.findall(r'>(.*?)<', tag, re.S)
            tagInfo[tagId[0]] = tagName[0][0]
            if tagId[0] not in smalltags.keys():
                smalltags[tagId[0]] = tagName[0]
        subUrl = re.findall(r'href="(.*?)"', titleInfoStr, re.S)
        url = rootUrl + subUrl[0]
        item['url'] = url
        item['question'] = question
        item['tag'] = tagInfo
        if u'0个回答' not in answerInfo:
            allTitles.append(item)
    return allTitles


# 获取问题和答案
def GetQuestionAnswers(allTitles):
    QuestionAnswers = []
    import time
    for item in allTitles:
        QuestionAnswer = {}
        if item['hasAnswer']:
            Answers = []
            url = item['url']
            try:
                time.sleep(0.5)
                user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
                headers = {
                    # 'Cookie': 'SUV=15036421120007811; SMYUV=1503642112001508; UM_distinctid=15e180dd23019d-0a186d63bebef8-24414032-fa000-15e180dd2314c; IPLOC=CN3100; SUID=DF82ABB41808990A00000000599FC201; ABTEST=3|1503642117|v1; SNUID=3F624B6BE0E5885216A56C48E0EDEC7C; weixinIndexVisited=1; JSESSIONID=aaalrBO0fbHqw4aJAVi4v; LSTMV=364%2C32; LCLKINT=1901; PHPSESSID=n22r9mafen98s0d8bi6vuo4ag6; SUIR=3F624B6BE0E5885216A56C48E0EDEC7C; sct=10; ppinf=5|15036845490|1504855090|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo1OlN1bm55fGNydDoxMDoxNTAzNjQ1NDkwfHJlZm5pY2s6NTpTdW5ueXx1c2VyaWQ6NDQ6bzl0Mmx1SHVnQ2h2dXR5UVVqeWFLd2Vfb2hRVUB3ZWl4aW4uc29odS5jb218; pprdig=FrV_V3ImaRCRWswYgnq9HS_kVnYgT3QGukdNr8nbBomC7ws4uyW_OVDQyRNPw54UCqY9cu8y4_pPsldYnja5r4EjpuRmBAyE1QrvTTfokvbmYdLehL6idggmSckKv3qCM51Y0ue039i9mtNMP1_Ec6OIa4l75yF87gmBh4m9G7E; sgid=31-30498125-AVmfzzJZBicSjRNuamaeWvZI; ppmdig=150364549100000045e887cdf81772ed1cf8a47eedc74007b',
                    'Host': 'wenwen.sogou.com',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'          }
                # proxy_support = urllib.request.ProxyHandler({'http': '222.220.113.4:3128'})
                # opener = urllib.request.build_opener(proxy_support)
                # opener.addheaders = [('User-Agent',
                #                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36')]
                # response = opener.open(url)
                request = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(request)
                html = response.read()
                questionAttrs = {'id': 'question_title_val'}
                answerAttrs = {'class': 'replay-info-txt answer_con'}
                bs = BeautifulSoup(html)
                # questions = bs.find_all(name='span',attrs=questionAttrs)
                questions = re.findall(r'question_title_val">(.*?)</span>', str(html,encoding = "utf-8"), re.S)
                question = questions[0]
                answers = bs.find_all(name='pre', attrs=answerAttrs)
                if answers:
                    for answer in answers:
                        answerStr = ''
                        if "<p>" in str(answer):
                            segements = re.findall(r'<p>(.*?)</p>', str(answer), re.S)
                            for seg in segements:
                                answerStr = answerStr + str(seg)
                            if answerStr.strip() != "":
                                Answers.append(answerStr.strip())
                        else:
                            noPanswer = re.findall(r'answer_con">(.*?)</pre>', str(answer), re.S)
                            Answers.append(noPanswer[0])
                    QuestionAnswer['answer'] = Answers
                QuestionAnswer['question'] = question
                QuestionAnswer['tag'] = item['tag']
                QuestionAnswer['hasAnswer'] = True
            except Exception as e:
                print(url)
                print(str(e))
        else:
            QuestionAnswer['question'] = item['question']
            QuestionAnswer['tag'] = item['tag']
            QuestionAnswer['answer'] = ''
            QuestionAnswer['hasAnswer'] = False
        QuestionAnswers.append(QuestionAnswer)
    return QuestionAnswers


# if __name__ == '__main__':
baseurl = "https://wenwen.sogou.com/cate/tag?"
rootUrl = 'https://wenwen.sogou.com'
# 问题分类标签
tagids = ['101', '146', '111', '163614', '50000010', '121', '93474', '9996', '148', '50000032', '135', '125', '9990',
          '465873']
global smalltags
smalltags = {}
# 遍历标签
for tagid in tagids:
    f =open('../input/' + str(tagid) + '_test.json', 'a',
                    encoding='utf-8')
    t = open('../input/' + str(tagid) + '_smalltag.json', 'a',
                    encoding="utf-8")
    # 每个标签拉n个页面
    print(u'标签:', tagid)
    for i in range(5000, 0, -1):
        tag = 'tag_id=' + tagid
        tp = '&tp=0'
        pno = '&pno=' + str(i)
        ch = '&ch=ww.fly.fy' + str(i + 1) + '#questionList'
        url = baseurl + tag + tp + tp + pno + ch
        print(url)
        QuestionAnswers = []
        QuestionAnswers = LoadPage(url)
        if QuestionAnswers:
            for qa in QuestionAnswers:
                jsonStr = json.dumps(qa, ensure_ascii=False)
                f.write(str(jsonStr) + '\n')
    # 保存tag
    json.dump(smalltags, t, ensure_ascii=False)
    t.close()
    f.close()