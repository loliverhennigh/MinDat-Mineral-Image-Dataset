

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
base_save_path = '/data/mindat-images/'

# read list of img urls
with open('img_url_list_converted.csv', 'r') as f:
  lines = f.readlines()
url_list = []
for l in lines:
  url_list.append(l.replace(' ','').split(',')) 

# make worker
url_queue = Queue(50)
def worker():
  while True:
    url_and_label = url_queue.get()
    url = url_and_label[0]
    label = url_and_label[1:-1]
    label.sort()
    name = base_save_path + '_'.join(label).replace('/','')
    if not os.path.isdir(name):
      os.mkdir(name)
    name = name + '/' + '_'.join(url.split('/')[3:])
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
