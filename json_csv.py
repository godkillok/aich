import json
import csv
from snownlp import SnowNLP
import pandas as pd
import re
from ahocorapy.keywordtree import KeywordTree

fs=['ai_challenger_oqmrc_testa.final_','ai_challenger_oqmrc_trainingset.final_','ai_challenger_oqmrc_validationset.final_']


def search(patterns,content):
    kwtree = KeywordTree(case_insensitive=True)
    for p in patterns:
        kwtree.add(p)

    kwtree.finalize()
    results = kwtree.search_all(content)
    result_list = []
    for result in results:
        result_list.append(result[0])
    return result_list

pun='''！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.'''
pun_l=[p for p in pun]


def in_char(query,passage):
    patterns=[q for q in query if q not in pun_l and q!=' ']
    common=search(patterns,passage)
    return len(set(common))/(len(set(patterns))+0.00000000001),len((common))/(len((patterns))+0.00000000001)


def in_words(query,passage):
    patterns=[q for q in query.split() if q not in pun_l and q!=' ']
    common=search(patterns,passage)
    return len(set(common))/(len(set(patterns))+0.00000000001),len((common))/(len((patterns))+0.00000000001)

def remove_other(text):
    tx=text
    if text.isdigit():
        return text
    else:
        if re.search('[\u4e00-\u9fa5]+\w*[\u4e00-\u9fa5]+',text).group(0)!=tx:
            print((re.search('[\u4e00-\u9fa5]+\w*[\u4e00-\u9fa5]+',text).group(0),tx))
        return re.search('[\u4e00-\u9fa5]+\w*[\u4e00-\u9fa5]+',text).group(0)

def clear_alternatives(text):
    url=text
    v_list = ' '.join(sorted(url.split('|')))
    if '不' in v_list or '没' in v_list:
        try:
            pos = [u for u in url.split('|') if '不' in u][0]
            if '/' in pos:
                pos = [u for u in pos.split('/') if '不' in u][0]
            if '|' in pos:
                pos = [u for u in pos.split('|') if '不' in u][0]
            pos = remove_other(pos)
            if pos[0] == '不':
                if len(pos) > 1:
                    return pos[1:].strip()+'|'+'不'+pos[1:].strip()+'|'+'无法确定'
                elif len(pos) == 1:
                    pos = [u for u in url.split('|') if '不' not in u and '无法' not in u][0]
                    pos = remove_other(pos)
                    if '是' != pos:
                        return pos+'|'+'不'+pos+'|'+'无法确定'
                    else:
                        return '是'+'|'+'不'+'是'+'|'+'无法确定'
            else:
                return url
        except Exception as e:
            # print(e)
            return url
    else:
        return url

for s in fs:
    with open('../input/{}'.format(s), 'r', encoding='utf8') as f:
        lines = f.readlines()
        print(len(lines))
        query_id = []
        passage = []
        query = []
        answer = []
        alternatives = []
        passage_len=[]
        query_in_char=[]
        query_in_word=[]
        query_in_char_set = []
        query_in_word_set = []
        ques_mark=[]
        for i in range(0, len(lines)):
            l = lines[i]
            ge = json.loads(l)

            que = SnowNLP(ge.get('query', '')).han
            query.append(que)


            query_id.append(ge.get('query_id',''))
            pas=SnowNLP(ge.get('passage','')).han
            try:
                pas=pas.split('？')[-1].strip()
            except:
                pass
            pas=pas.replace(que,'')


            if len(pas)<2:
                pas = SnowNLP(ge.get('passage', '')).han
                print(ge.get('passage',''))
                print(ge.get('query', ''))
                print(ge.get('answer',''))
                print('---')
            passage.append(pas)

            answer.append( ge.get('answer',''))
            gege=clear_alternatives(ge.get('alternatives', ''))
            alternatives.append(gege)
            passage_len.append(1 if len(passage)>150 else len(passage)/150)
            ques_mark.append(1 if '？' in pas else 0)
            char_set,char=in_char(que,pas)
            word_set,word=in_words(que,pas)
            query_in_char.append(char)
            query_in_word.append(word)
            query_in_char_set.append(char_set)
            query_in_word_set.append(word_set)
        d={
            'query_id':query_id,
            'passage':passage,
            'query':query,
            'answer':answer,
            'alternatives':alternatives,

        }
        if 'train' in s:
            file_name='train.csv'
        elif 'test' in s:
            file_name='test.csv'
        elif 'validation' in s:
            file_name = 'validation.csv'
        pd.DataFrame.from_dict(d)[['query_id','passage_len','ques_mark','passage','query','alternatives','query_in_char','query_in_word','query_in_char_set','query_in_word_set','answer']].to_csv('../input_1/{}'.format(file_name),index=False,index_label=False,header=True)
            