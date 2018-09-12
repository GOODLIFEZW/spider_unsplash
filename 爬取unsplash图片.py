import requests
from queue import Queue
import threading
import time
import random
import json
import os
import urllib 

url_queue=Queue()   # 使用队列保存图片url，确保线程同步
THREAD_NUM=5
IMAGE_PATH='D:/Unsplash/'

class Unspalsh(threading.Thread):

    def __init__(self,thread_id):
        threading.Thread.__init__(self)
        self.thread_id=thread_id

    def run(self):
        while not url_queue.empty():
            url=url_queue.get()
            self.get_img_url(url)
            time.sleep(random.randint(3,5))  
        
    def get_img_url(self,url):
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
        }
        reponse=requests.get(url,headers=headers)
        img_url=json.loads(reponse.text)[0]['urls']['full']
        self.save_img(img_url)

    def save_img(self,img_url):
        if not os.path.exists(IMAGE_PATH):
            os.mkdir(IMAGE_PATH)
        file_name=IMAGE_PATH+img_url.split('-')[1]+'.jpg'
        try:
            # 下载图片，保存到指定文件夹中
            urllib.request.urlretrieve(img_url,filename=file_name)
        except requests.exceptions.Timeout:
            print('超时')

def get_all_url():
    base_url='https://unsplash.com/napi/photos?page={}&per_page=1&order_by=latest'
    page=1
    while page<=50:
        img_url=base_url.format(page)
        url_queue.put(img_url)
        page=page+1

if __name__=='__main__':
    get_all_url()
    for i in range(THREAD_NUM):
        unspalsh=Unspalsh(i+1)
        unspalsh.start()