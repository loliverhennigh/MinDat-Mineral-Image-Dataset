

from io import StringIO, BytesIO
import requests
from lxml import etree
import os
import sys
import imghdr
from tqdm import *
from Queue import Queue
from threading import Thread

# base path to save images
base_save_path = './data/mindat-images/'

# read list of img urls
with open('img_url_list.csv', 'r') as f:
  lines = f.readlines()
url_list = []
for l in lines:
  url_list.append(l.split(',')[0]) 

# make worker
url_queue = Queue(50)
def worker():
  while True:
    url = url_queue.get()
    name = base_save_path + '_'.join(url.split('/')[3:])
    if not os.path.exists(name):
      img_data = requests.get(url).content
      with open(name, 'wb') as handler:
        handler.write(img_data)
    url_queue.task_done()
   
for i in xrange(100):
  t = Thread(target=worker)
  t.daemon = True
  t.start()

# get all 900,000 urls
for url in tqdm(url_list):
  url_queue.put(url)
url_queue.join()
