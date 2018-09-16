# -*- coding: utf-8 -*-

import urllib.request
import time
import json
import jieba

token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
# 1.获取token
api_key =  "mz34N7Uxhl13CX0oDc3Pbzf6"

api_secert = "yr8ssh7QFmqL0nq9XGqlYWTa0GRXKsci"


token_url = token_url % (api_key, api_secert)

r_str = urllib.request.urlopen(token_url).read()
r_str = str(r_str, encoding="utf-8")
token_data = json.loads(r_str)
token_str = token_data['access_token']
url_all = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?access_token=' + str(token_str)

fs=['ai_challenger_oqmrc_validationset.seg_']

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
query_list=[]

for s in fs:
    count=0
    with open('../input/{}'.format(s),'r',encoding='utf8') as f:
        lines = f.readlines()
        print(len(lines))
        result=[]

        for i in range(0,len(lines)):
            l=lines[i]

            if count%100==0:
                print(count,len(lines),s)
            ge = json.loads(l)
            query_id=ge.get('query_id')
            passage=ge.get('passage')
            query = ge.get('query')
            retry=10
            if query_id not in query_list:
                # print('not in {}'.format(query_id))
                count += 1
                query_list.append(query_id)
            else:
                print(query_id)
                continue

            if ge.get('retry')==True:
                ge['passage']=' '.join(jieba.cut(passage))

            retry=10

            if  ge.get('retry')==True:
                ge['query'] = ' '.join(jieba.cut(query))

            l=json.dumps(ge,ensure_ascii=False)

            with open('../input/{}'.format(s.replace('seg_','final_')),'a',encoding='utf8') as f:
                f.writelines(l+'\n')

