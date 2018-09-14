# coding:utf8


import urllib.request
import os
import time
import hashlib
import datetime
import hashlib
import xlrd
import jieba
from email.mime.text import MIMEText
import smtplib
import base64
import requests
from lxml import etree

 

start = time.clock()

print("                                        程序启动成功,3秒后开始采集   ")
print("\r")
print("\r")
print("\r")
time.sleep(3)

print(" 正在读取分词库...........")
# dededata = xlrd.open_workbook('dededic.xlsx')
# dedetable = dededata.sheets()[0]
# dederesult= dedetable.col_values(1)
print(" Success！")



print("\r")
print(" 正在获取采集URl......")
def ht(url='',words=''):
    s = requests.session()
    s.headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"
    if url=='':
        url = "http://www.120ask.com/list/"
    query = url+words
    search_result=s.get(query)
    search_html = search_result.content
    html_obj = etree.HTML(search_html)
    return html_obj

html_obj=ht()
fenleiList=html_obj.xpath("/html/body/div[*]/div[*]/div/div[*]/div/div/div[*]/div[*]/div[*]/p/a")
fenleiItems=[]
for fenlei in fenleiList:
    ur=fenlei.attrib.get('href','')
    if 'http' in ur:
        fenleiItems.append(ur)


for pa in range(100):
    url='http://www.120ask.com/list/over/'
    url1=url + '{}/'.format(pa)
    html_obj=ht(url1)
    per_list=html_obj.xpath("//*[@id='list']/div[1]/div[3]/ul/li[*]/div[1]/p/a")
    questions=[]
    for per in per_list:
        ur = per.attrib.get('href', '')
        if 'http' in ur:
            questions.append(ur)
        print(url1)

    for q in questions:
        html_obj = ht(q)
        title = html_obj.xpath("//*[@id='d_askH1']//text()")[0].strip().replace('\n','')
        detail=str(html_obj.xpath("/html/body/div[1]/div[5]/div[2]/div[3]/div[2]/p[1]//text()")).split('健康咨询描述：')[1].strip().replace('\n','')
        answer=str(html_obj.xpath("/html/body/div[1]/div[5]/div[2]/div[7]/div[1]/div[2]/div[2]//text()"))
        answer =answer.split('意见：')[1].strip().replace('\n','')







print("\r")

print(" Success！")



aaa=11
bbb=111

for fl in fenleiItems:


    try:
        mypagenum =  int(HttpGet(fl+"over/").find(".h-page").find("a").eq(-1).attr("href")[len(fl+"over/"):][::-1][1:][::-1])
    except Exception:
        mypagenum=1

    
    
    for psize in range(1,mypagenum):
          try:
             purl=fl+"over/"+str(psize)+"/"
             phtml=HttpGet(purl)
             mlist=phtml.find(".h-color")
             print("")
             print("")
             print("----------------- 准备抓取第 "+str(psize)+" 页的数据 -------------------------")
             
             
            
             for mitem in mlist.items():
                 link = mitem.find(".q-quename").attr("href")
                 content=HttpGet(link)

                 title=content.find("#d_askH1").html()
                 question=content.find("#d_msCon").find("p").html()[60:]
                 classname=content.find(".b_route").find("a").eq(-1).find("span").html()
                 department=content.find(".b_route").find("a").eq(-2).html();
                 qaid=Md5(link)
                 updatetime = datetime.datetime.now()
                 
                 cur.execute("select count(*) from question where qaid= %s",[qaid])
                 rowresult = str(cur.fetchall())
                 
                 fenci=[]

                 seg_list = jieba.cut(title)  
                 jiebares=",".join(seg_list).split(',')
                 for jb in jiebares:
                     for dede in dederesult:
                         if jb==dede:
                             fenci.append(jb)

                 keyword=','.join(fenci)

                 if rowresult!="((0,),)":
                     continue

                 

                 
                 title,question
                 
                 aaa+=1
                 
                
                 
                 
                 
                 ans=content.find(".b_answerli")
                 g=0
                 for x in ans.items():
                     g+=1
                     if str(x.attr("class"))!="b_answerli":
                         continue
                     state=0
                     if g==1:
                        state=1

                     username=x.find(".b_sp1").find("a").html()
                     if username==None or username=="":
                         username="未知"
                     nickname=x.find(".b_sp1").html()[-100:][0:2]
                     gooduse=x.find(".b_answertl").find("span").eq(1).html()
                     if "擅长" not in gooduse:
                         gooduse="未知"
                     pp=x.find(".crazy_new").find("p").html()
                    
                     bingqing=pp[pp.find("病情分析：<br/>")+16:pp.find("指导意见：<br/>")]
                     zhidao = pp[pp.find("指导意见：<br/>")+16:]
                   
		     
                    
                     
                     print("\n")
                     print(" 入库成功:" + " ："+str(title))
                     bbb+=1


          except Exception:
              continue
        







end = time.clock()
mytime= (end-start)









print('''
             


                                      ,==.              |~~~       全部抓取完成
                                     /  66\             |
                                     \c  -_)         |~~~        '''+"本次一共抓取了 "+str(aaa)+" 个问题"+'''
                                      `) (           |
                                      /   \       |~~~           '''+"本次一共抓取了 "+str(bbb)+" 个答案"+'''
                                     /   \ \      |
                                    ((   /\ \_ |~~~              '''+"本次一共用了  "+str(mytime/3600).split('.')[0]+" 个小时"+'''
                                     ||  \ `--`|
                                     / / /  |~~~
                                ___ (_(___)_|  



    ''')





res=input()
