#encoding=utf-8
#coding=utf-8
import requests
import jieba
import emoji
import jieba
import threading
import os
import wordcloud 

#读取停用词
stopWordList = open('stopWord.txt').read().splitlines()

#获取20条评论多线程类
class myThread (threading.Thread):
    def __init__(self, name,num,file,av):
        threading.Thread.__init__(self)
        self.name = name
        self.num = num
        self.file=file
        self.av=av
    def run(self):
        print ("开始线程：" + self.name)
        get20Text(self.num,0,self.file,self.av)
        print ("退出线程：" + self.name)



 #定义个函数式用于分词
def jiebaClearText(text):
    
    jieba_list=jieba.cut(text,cut_all=False)
    
    #return ' '.join(list)
    outstr=""
    for word in jieba_list:
        if word not in stopWordList:
            outstr += " "
            outstr += word
                 
    return outstr   



#获取20条评论函数
def get20Text(nextnum,num,ff,av):
    payload = {'oid': av,'type': '1', 'next': nextnum}

    try:

        
         response = requests.get('https://api.bilibili.com/x/v2/reply/main', params=payload)
         r_json = response.json()
         print(response.url)
         stairs=nextnum
         #12690245
         print(len(r_json['data']['replies']))
         for i in r_json['data']['replies']:
             stairs+=1
             
             try:
                 print("第"+str(stairs)+"楼："+emoji.demojize(str(i['content']['message'])))
                 ff.write(jiebaClearText(emoji.demojize(i['content']['message'])))
             except UnicodeEncodeError:
                 print("[error]编码错误，跳过此条信息")
            
                   


    except:
        print("[error]请求出现问题，正在重试。。。。")
        if num >=10:
            print("[warning]次数超时，跳过")
        else:
            num+=1
            get20Text(nextnum,num,ff,av)







#读取视频信息，获得全部评论
def getAllComment(av,f):
    next_num=0
    text_num=0



    #第一次请求，获取全部评论数
    payload = {'oid': av,'type': '1', 'next': '0'}

    response = requests.get('https://api.bilibili.com/x/v2/reply/main', params=payload)

    print("共"+str(response.json()['data']['cursor']['prev'])+"楼")
    
    text_num =response.json()['data']['cursor']['prev']

    threads=[]
    while next_num <= text_num-1:
       
       thread = myThread("Thread-"+str(next_num), next_num,f,av)
       thread.start()
       threads.append(thread)
       next_num+=20
   

    for t in threads:
        t.join(30)

    print("单一视频全部进程已结束")

    


   
    


 #生成词云图
def makeWordCloud(cloudText,filename):
    if(cloudText == "" ):
        print("评论为空")

    else:
        w=wordcloud.WordCloud(
            font_path='C:/Windows/Fonts/simkai.ttf',
            background_color='white',
            width=4096,
            height=2160,
            max_words=1000,
        )
        w.generate(cloudText)
        w.to_file(filename+".png")
        os.startfile(filename+".png")
        #os.startfile(av+".txt")
    






if  __name__=="__main__":
    print("-----------------------------------------------------------")
    print(" 11          11    11    11    11          11    11    11  ")
    print(" 11                11          11                11        ")
    print(" 111111      11    11    11    111111      11    11    11  ")
    print(" 11    11    11    11    11    11    11    11    11    11  ")
    print(" 11    11    11    11    11    11    11    11    11    11  ")
    print(" 111111      11    11    11    111111      11    11    11  ")
    print("-----------------------------------------------------------")
    print("                                            bilibili@圆无边")
    #输入视频号
    av = input("输入将分析视频号：av")
    #创建文件
    fff = open(av+'.txt', 'w')
    getAllComment(av,fff)

    fff.close()

    #读取要分析的文本，读取格式
    text=open(av+'.txt').read()
    print("正在生成图片。。。。")
    makeWordCloud(text,av)
