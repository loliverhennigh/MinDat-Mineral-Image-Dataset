

from io import StringIO, BytesIO
import requests
from lxml import etree
import os
import sys
import imghdr
from tqdm import *
from Queue import Queue
from threading import Thread

# checks if string is valid ascii
def is_ascii(s):
  return all(ord(c) < 128 for c in s)

# base path
base_path = 'https://www.mindat.org/'

# list of urls and mineral types
img_urls = []
mineral_types = []
all_minerals = []

# make worker
url_queue = Queue(100)
def worker():
  while True:
    url = url_queue.get()
    try:
      page = requests.get(url, timeout=60)
    except:
      # if url is bad
      url_queue.task_done()
    html = etree.HTML(page.content)
    # find image url, if empty break
    img_url = html.xpath('.//img[@id="mainphoto"]')
    if not (len(img_url) == 0):
      img_url = img_url[0].attrib['src']
      img_url = base_path + img_url
      # find mineral names 
      html_mineral = html.xpath('.//meta[@property="og:title"]')[0]
      html_mineral = html_mineral.attrib['content']
      minerals = [html_mineral]
      # check if valid name
      valid_name = True
      for m in minerals:
        if not is_ascii(m):
          valid_name = False
      if valid_name:
        # possibly add to list of all minerals
        for m in minerals:
          if m not in all_minerals:
            all_minerals.append(m)
        # add them to list
        mineral_types.append(minerals)
        img_urls.append(img_url)
    url_queue.task_done()
   
for i in xrange(100):
  t = Thread(target=worker)
  t.daemon = True
  t.start()

# get all 900,000 urls
for i in tqdm(xrange(900)):
  for j in tqdm(xrange(1000)):
    url_queue.put(base_path + 'photo-' + str(j + 1000*i) + '.html')
  url_queue.join()
  print("saving URLs")
  # save all data every 10000 urls
  img_url_file = open("img_urls/img_url_list_" + str(i).zfill(5) + ".csv", "w")
  for i in xrange(len(img_urls)):
    img_url_file.write(img_urls[i] + ', ')
    for m in mineral_types[i]:
      img_url_file.write(m + ', ')
    img_url_file.write('\n')
  img_url_file.close()
  img_urls = []
  mineral_types = []

