# coding=utf-8

import requests
import time
import datetime
from bs4 import BeautifulSoup
import os

# @创建gallery文件夹
# @input:GALLERY_NAME gallery保存的文件夹
# @output:
def mkdir(GALLERY_NAME):
    GALLERY_NAME = GALLERY_NAME.strip()
    GALLERY_NAME = GALLERY_NAME.rstrip("\\")

    if not os.path.exists(GALLERY_NAME):  # 如果不存在则创建目录
        print(GALLERY_NAME + ' Success')   # 创建目录操作函数
        os.makedirs(GALLERY_NAME)
        return True
    else:  # 如果目录存在则不创建，并提示目录已存在
        print(GALLERY_NAME + ' existence')
        return False
    
def bcyTopDownloader(GALLERY_START_URL):   
    #保存ehentai的cookie文件地址
    cookie_file = "bcy_cookie.txt"
    
    if os.path.exists(cookie_file):
        #如果cookies文件存在则直接读取cookie
        bcy_cookies = {}
        
        with open(cookie_file,'r',buffering = 4*1024) as fp:
            for line in fp.read().split(';'):
                name,value = line.strip().split('=',1)
                bcy_cookies[name] = value
            fp.flush()
       
        print('load cookies is Success')
    else: 
        print('you have no cookie')
  
    print ("bcy cookies:" + str(bcy_cookies))
    
    #user_head
    agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 OPR/46.0.2597.57'
    user_head={
        #'Host':"153.180.26.202:10428",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
        'Accept-Encoding': "gzip, deflate, sdch, br",
        'Accept-Language': "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2",
        'Cache-Control':'max-age=0',
        "Connection": "keep-alive",
        'Referer': 'https://bcy.net/start',
        'User-Agent': agent    
    }
    
    
    # 文件夹的名字
    GALLERY_NAME = '半次元' + time.strftime('%Y-%m-%d')
    
    #新建用户文件夹
    mkdir(GALLERY_NAME)
    
    
    #浏览器打开首页
    gallery_content = requests.get(GALLERY_START_URL,cookies=bcy_cookies,headers=user_head,timeout=9).text.encode('utf-8')   
    
    #得到首页的soup的对象
    gallery_soup = BeautifulSoup(gallery_content,'html5lib')
    
    # 得到所有的作品入口
    all_work = gallery_soup.findAll('li',class_ = 'l-work-thumbnail')
    top_index = 1
    for work in all_work:
        
        top_index % 10 ==0 and time.sleep(15)
            
            
        work_a = work.find('div',class_ = 'work-thumbnail__topBd').find('a')
        title = work_a['title']
        
        #去掉保存到本地图片文件名中非法字符
        unvalid_str = '<>,\/|,:,"",*,?'
        for ch in unvalid_str:
            title = title.replace(ch,'') 
        title = title.strip()    
              
        work_url = 'https://bcy.net' + work_a['href']
        print(work_url)
        
        #新建作品
        WORK_FOLD_NAME = GALLERY_NAME + '\\' +str(top_index).zfill(3) + '_' + title
#        print(WORK_FOLD_NAME)
        mkdir(WORK_FOLD_NAME)
        
        #得到作品html对象
        image_content = requests.get(work_url,cookies=bcy_cookies,headers=user_head,timeout=20).text.encode('utf-8') 
        
        #得到作品soup对象
        image_group_soup = BeautifulSoup(image_content,'html5lib')
    
        #每一个图片的soup对象
        image_group_div = image_group_soup.findAll('img',class_ = 'detail_std')
        
        #记录爬去图片的标号 
        image_index = 0
        
        #遍历每一个有图片的image div
        for image in image_group_div:
            image_url = image['src'] #图片的URL
            image_url = image_url[:-5] #图片URL去掉后缀得到真正的RAW图片
            
            #获取图片图像，注意图片是资源所用 stream设置为True
            pic = requests.get(image_url, stream=True,cookies=bcy_cookies, headers=user_head,timeout=12)
            
            #图片保存在本地的路径
            file_local_url = WORK_FOLD_NAME + '\\' +str(image_index).zfill(2) +'.jpg'
            
            #图片已存在则直接continue
            if os.path.exists(file_local_url):
                print('pic has been downloaded!')
                continue
            else:
                print('pic is downloaded, start to writing to local ')    
                # 推荐使用witho open,避免忘记进行fp.close()操作，buffering设置是为了IO加速
                with open(file_local_url, 'wb',buffering = 4*1024) as fp:
                    fp.write(pic.content) #写入file_local_url内容到图片
                    fp.flush()  
                print(image_url +' download Successful')
                
            image_index = image_index +1
        
        
        top_index = top_index +1
       
        
                
    
    

if __name__ == '__main__':
    
    GALLERY_START_URL = "https://bcy.net/coser/toppost100"
    # 程序开始的时间
    start_time = datetime.datetime.now()
    
    bcyTopDownloader(GALLERY_START_URL)
    
    # 程序的结束时间
    end_time = datetime.datetime.now()
            
    # 打印程序运行时间
    print('Time cost: ' + str((end_time-start_time).seconds))
    
    print('All work is finished!')