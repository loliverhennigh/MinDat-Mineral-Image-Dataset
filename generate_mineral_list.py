

import os
import sys
from tqdm import *

# helper function
def _convert_string_to_mineral_list(string):
  string = string.lower()
  string = string.replace(' ','')
  start = -1 
  end = -1 
  if 'var' in string:
    for i in xrange(len(string)):
      if string[i] == '(':
        start = i
    string = string[:start]

  return string 

with open('img_url_list.csv', 'r') as f:
  lines = f.readlines()

# split url out
all_minerals = []
all_minerals_count = dict()
for i in xrange(len(lines)):
  new_line = lines[i].split(',')
  for j in xrange(len(new_line)-1):
    new_line[j+1] = _convert_string_to_mineral_list(new_line[j+1])
  for j in xrange(len(new_line)-2):
    if new_line[j+1] not in all_minerals:
      all_minerals.append(new_line[j+1])
      all_minerals_count[new_line[j+1]] = 1
    else:
      all_minerals_count[new_line[j+1]] += 1
  lines[i] = new_line
all_minerals.sort()
    
all_minerals_file = open("all_minerals.csv", "w")
number_of_mins = 0
for m in all_minerals:
  if all_minerals_count[m] > 1000:
    if m != '':
      all_minerals_file.write(m + ', ')
      number_of_mins += 1
print(number_of_mins)

