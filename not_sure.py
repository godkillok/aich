
import json
import re
from collections import Counter
ans=[]
co=0
cr=0
c3=0
with open('../input/ai_challenger_oqmrc_trainingset.json','r',encoding='utf8') as f:
    lines=f.readlines()
    for l in lines:
        ge=json.loads(l)
        url=ge.get('answer')

        if '无法确定'==url and ('看你' in ge.get('passage') or '具体'in ge.get('passage') or '综合考虑' in ge.get('passage') ):
            co+=1
            if co<20:
                print(l)

        if '无法确定'==url and ('看你' not in ge.get('passage') ):
            c3+=1
            if c3<20:
                print(l)
        if '无法确定'!=url and ('看你' in ge.get('passage') or '具体'in ge.get('passage') or '综合考虑' in ge.get('passage') ):
            cr+=1
            if cr<20:
                print(l)
print(cr,co)

with open('../input/ai_challenger_oqmrc_trainingset.json','r',encoding='utf8') as f:
    count=0
    lines = f.readlines()
    result = []
    for i in range(len(lines) - 1, 0, -1):
        l = lines[i]
        count += 1
        ge = json.loads(l)
        passage = ge.get('passage')
        query = ge.get('query')
        retry = 10
        retry=ge.get('')