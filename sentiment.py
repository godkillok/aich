# -*- coding: utf-8 -*-

import urllib.request
import time
import json
import jieba
import re
from gensim import corpora
from gensim import corpora, models, similarities
import numpy as np

fs=['ai_challenger_oqmrc_trainingset.final_']
words='的了么吗'
#,'ai_challenger_oqmrc_validationset.final_'
stop_words=[s for s in words]
api=[
    # {'api_key' : "mz34N7Uxhl13CX0oDc3Pbzf6",
    # 'api_secert' : "yr8ssh7QFmqL0nq9XGqlYWTa0GRXKsci"},
    {'api_key': 'hGs3TEt3sN3XcI3VyIAyuTQp',
     'api_secert': 'P7tCqnwMBEPs6bpEa4TOr4voTtAtTdxQ'}
]




url_all=''
def get_url(api_key, api_secert):
    global url_all
    token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
    # 1.获取token
    token_url = token_url % (api_key, api_secert)

    r_str = urllib.request.urlopen(token_url).read()
    r_str = str(r_str, encoding="utf-8")
    token_data = json.loads(r_str)
    token_str = token_data['access_token']
    url_all = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=' + str(token_str)
    # return url_all

url_all_list=[]
for u in api:
    url_all_list.append(get_url(u.get('api_key'),u.get('api_secert')))


def remove_punctuation(line):
  rule = re.compile(r"[^a-zA-Z0-9 \u4e00-\u9fa5]")
  line = rule.sub('',line)
  return line

def sim(text,query):
    texts=[]
    query = remove_punctuation(query)

    texts.append([q for q in query.split(' ') if q not in stop_words])

    for t in text:
        t = remove_punctuation(t)
        texts.append([q for q in t.strip().split(' ')if q not in stop_words])

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    index = similarities.MatrixSimilarity(corpus)
    id_=np.argmax(index[corpus[0]][1:])
    mos=text[id_]
    return mos

def  senti(word1,url_all):
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


    return res.get('items')[0]

for s in fs:
    count=0
    with open('../input/{}'.format(s),'r',encoding='utf8') as f:
        lines = f.readlines()
        result=[]
        for l in lines:

            # time.sleep(1.01/5)
            if count%100==0:
                print(count,len(lines),s)
            ge = json.loads(l)
            passage=ge.get('passage')
            query = ge.get('query')
            ans = ge.get('answer')

            if ge.get('retry','')!=True:

                if len(passage.split('。'))>1:
                    text=passage.split('。')
                    mos = sim(text, query)
                elif len(passage.split('，'))>1:
                    text = passage.split('。')
                    mos = sim(text, query)
                else:
                    mos=passage
                # if count%len(api)==0:
                if ge['query_id']<22940:
                    continue
                count += 1
                time.sleep(1.01 / 5)
                retry=10
                baidu={}
                while retry > 0:
                    try:
                        baidu = senti(mos, url_all)
                        retry = -1
                    except Exception as e:
                        time.sleep(1 / 4)
                        retry -= 1
                        if retry < 1:
                            ge['senti_retry'] = True
                            print(passage)
                            print(e)

                # elif count%len(api)==1:
                #     baidu =senti(mos, url_all_list[1])


                ge['passage'] = mos
                ge['answer_baidu_score'] = baidu
                ge['answer_type'] = baidu.get('sentiment')

                if count<300:
                    print(mos)
                    print(query)
                    print(ans)
                    print(baidu.get('sentiment'))
                    print('----')


                with open('../input/{}'.format(s+'00'), 'a', encoding='utf8') as f:
                    f.writelines(json.dumps(ge,ensure_ascii=False)+'\n')






