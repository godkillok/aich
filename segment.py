# -*- coding: utf-8 -*-

import urllib.request
import time
import json
import jieba
token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
# 1.获取token
api_key = 'hGs3TEt3sN3XcI3VyIAyuTQp'
api_secert = 'P7tCqnwMBEPs6bpEa4TOr4voTtAtTdxQ'

token_url = token_url % (api_key, api_secert)

r_str = urllib.request.urlopen(token_url).read()
r_str = str(r_str, encoding="utf-8")
token_data = json.loads(r_str)
token_str = token_data['access_token']

url_all = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?access_token=' + str(token_str)
fs=['ai_challenger_oqmrc_trainingset.json','ai_challenger_oqmrc_testa.json','ai_challenger_oqmrc_validationset.json']

def  segm(word1):

    data2 = {'text': word1}
    post_data = json.dumps(data2)
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   'Content-Type': 'application/json'}
    req = urllib.request.Request(url=url_all, data=bytes(post_data, encoding="gbk"), headers=header_dict)
    res = urllib.request.urlopen(req).read()
    # print(res)
    r_data = str(res, encoding="GBK")
    # print(r_data)
    res = json.loads(r_data)

    seg = []
    for i in res.get('items'):
        seg.append(i.get('item'))
    sentence = ' '.join(seg)
    return str(sentence)

for s in fs:
    count=0
    with open('../input/{}'.format(s),'r',encoding='utf8') as f:
        lines = f.readlines()
        result=[]
        for l in lines:
            count+=1

            if count%100==0:
                print(count,len(lines),s)
            ge = json.loads(l)

            passage=ge.get('passage')
            query = ge.get('query')
            retry=10

            time.sleep(1.01 / 5)
            while retry>0:
                try:
                    ge['passage']=segm(passage)
                    retry=-1
                except Exception as e:
                    time.sleep(1/4)
                    retry-=1
                    if retry<1:
                        ge['retry']=True

                        print(passage)
                        print(e)

            retry=10
            while retry>0:
                try:
                    ge['query']=segm(query)
                    retry=-1
                except Exception as e:
                    time.sleep(1/4)
                    retry-=1
                    if retry<1:
                        print(query)
                        ge['retry']=True
                        print(e)


            result.append(json.dumps(ge,ensure_ascii=False))
            if count%500==0:
                with open('../input/{}'.format(s.replace('json','seg')),'a',encoding='utf8') as f:
                    for l in result:
                       f.writelines(l+'\n')
                result=[]

