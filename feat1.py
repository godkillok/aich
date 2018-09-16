import json
import re
from collections import Counter
web_site=[]
class_label={
'health':['120ask','hospit','ziyimall','youlai','dzys','yaolan','uooyoo','5h','health','fh21','baobao','doctor','120','kang','.mama.','.39','haodf','baby','xywy'],
    'gov':['gov'],
    'sports':['sports','fitness'],
    'games':['game','520apk'],
    'news':['news','sc.'],
    'edu':['gaosan','zybang','learn','edu/','gaokao','mofangge'],
    'law':['law','110'],
    'ecom':['taobao','itmop','1688','.zol.','consumer','price','product','smzdm','apple','huawei'],
    'house':['house','fang.'],
    'auto':['auto','car','che'],
    'wenwen':['zhidao','wenwen','ask','zhinan']
}

with open('../input/ai_challenger_oqmrc_trainingset.json','r',encoding='utf8') as f:
    lines=f.readlines()
    for l in lines:
        ge=json.loads(l)
        url=ge.get('url')
        flag=True
        for (k,v_list) in class_label.items():
            for v in v_list:
                if v in url:
                    web_site.append(k)
                    flag=False
                    break
        if flag:
            web_site.append(url.split('//')[1].split('/')[0])
            # web_site.append(url.split('//')[1].split('/')[0].split('.')[1])
    ct=Counter(web_site)
print(ct.most_common(1000))

ans=[]
posi=[]

def semtition(item):
    item.get('')


def remove_other(text):
    tx=text
    if text.isdigit():
        return text
    else:
        if re.search('[\u4e00-\u9fa5]+\w*[\u4e00-\u9fa5]+',text).group(0)!=tx:
            print((re.search('[\u4e00-\u9fa5]+\w*[\u4e00-\u9fa5]+',text).group(0),tx))
        return re.search('[\u4e00-\u9fa5]+\w*[\u4e00-\u9fa5]+',text).group(0)

with open('../input/ai_challenger_oqmrc_trainingset.json','r',encoding='utf8') as f:
    lines=f.readlines()
    print(len(lines))



    for l in lines:
        ge=json.loads(l)
        url=ge.get('alternatives')

        v_list=' '.join(sorted(url.split('|')))
        if '不'  in v_list or '没' in v_list:
            ans.append('不')
            try:
                pos=[u for u  in url.split('|') if '不'  in u  ][0]
                if '/' in pos:
                    pos = [u for u in pos.split('/') if '不' in u][0]
                if '|' in pos:
                    pos = [u for u in pos.split('|') if '不' in u][0]
                pos=remove_other(pos)
                if pos[0] == '不':
                    if len(pos) > 1:
                        posi.append(pos[1:].strip())
                    elif len(pos)==1:
                        pos= [u for u  in url.split('|') if '不' not in u and '无法' not in u  ][0]
                        pos = remove_other(pos)
                        if '是' !=  pos:
                            semtition(ge)

            except:
                pass
                # print( url.split('|'))
                # print(ge)

        else:
            ans.append(v_list)
    ct=Counter(ans)
print(ct.most_common(1000))
print(list(set(posi)))
#


# '看你'
# '看后面考试的时候教练会不会与你联系'
# '看个人'
''