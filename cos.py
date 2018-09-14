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
# print(ct.most_common(1000))

ans=[]
with open('../input/ai_challenger_oqmrc_trainingset.json','r',encoding='utf8') as f:
    lines=f.readlines()
    for l in lines:
        ge=json.loads(l)
        url=ge.get('alternatives')
        flag = True
        v_list=' '.join(sorted(url.split('|')))
        if '不'  in v_list or '没' in v_list:
            ans.append('不')
            flag = False
        else:
            ans.append(v_list)
    ct=Counter(ans)
# print(ct.most_common(1000))

ans=[]
co=0
cr=0
with open('../input/ai_challenger_oqmrc_trainingset.json','r',encoding='utf8') as f:
    lines=f.readlines()
    for l in lines:
        ge=json.loads(l)
        url=ge.get('answer')

        # if '无法确定'==url and (('看你' in ge.get('passage') and '都' not in ge.get('passage') and '如果' not in ge.get('passage') and '的话' not in ge.get('passage')) ):
        #     co+=1
        #     if co<20:
        #         print(l)
        if '无法确定'!=url and (('看你' in ge.get('passage') and '查看' not in ge.get('passage') and '都' not in ge.get('passage') and '如果' not in ge.get('passage') and '的话' not in ge.get('passage')) ):
            cr+=1
            if cr<20:
                print(l)
print(cr,co)

# '看你'
# '看后面考试的时候教练会不会与你联系'
# '看个人'
''