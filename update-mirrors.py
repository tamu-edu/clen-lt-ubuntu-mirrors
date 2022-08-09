from operator import attrgetter
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
from typing import List
import threading

#### Configuration ####

country = 'United States' # Set to '' for all
max_count = 10

## End Configuration ##

speedRegex = r'([0-9]+) (Gbps|Mbps|Kbps)'

class AptMirror:
  uri: str
  country: str
  speed: int
  latency: int

  def __init__(self, country: str, uri: str, speed: int):
    self.uri = uri
    self.country = country
    self.speed = speed

def average(lst):
  return sum(lst) / len(lst)

def update_latency(mirror: AptMirror):
  try:
    latency = requests.get(mirror.uri, timeout=20).elapsed.microseconds
    mirror.latency = latency / 1000
  except:
    mirror.latency = -1

def update_latencies(mirrors: List[AptMirror]):
  threads = list()
  for mirror in mirrors:
    x = threading.Thread(target=update_latency, args=(mirror,))
    threads.append(x)
    x.start()
  
  for index,thread in enumerate(threads):
    thread.join()

def parse_speed(speedStr):
  m = re.search(speedRegex, speedStr)
  if not m:
    return 0
  speed = int(m.group(1))
  match m.group(2):
    case 'Gbps':
      speed = speed * 1000000
    case 'Mbps':
      speed = speed * 1000
  return speed

def read_ignore_list():
  ignore_mirrors = []
  with open('ignore_mirrors.txt') as f:
    for line in f:
      ignore_mirrors.append(line)
  return ignore_mirrors

ignore_mirrors = read_ignore_list()
html = requests.get('https://launchpad.net/ubuntu/+archivemirrors')
parsed_html = BeautifulSoup(html.text, "lxml")
table = parsed_html.find('table', { 'id': 'mirrors_list' })
table_rows = table.find_all('tr')
current_country = ''
mirrors: List[AptMirror] = list()
for row in table_rows:
  if row.has_attr('class') and row['class'] == ['head']:
    current_country = row.find('th').get_text()
    continue
  elif row.has_attr('class') and row['class'] == ['section-break']:
    continue
  else:
    if country != '' and current_country != country:
      continue
    row_parts = row.find_all('td')
    url = ''
    speed = row_parts[2].text
    for a in row_parts[1].find_all('a'):
      if a.text == "https" or a.text == "http":
        url = a['href']
        break
    if url != '' and not url in ignore_mirrors:
      mirror = AptMirror(country=current_country, uri=url, speed=parse_speed(speed))
      update_latency(mirror)
      mirrors.append(mirror)

# update_latencies(mirrors=mirrors)

mirrors.sort(key = lambda x: (-x.speed, x.latency))
count = 0
for mirror in mirrors:
  if count > max_count:
    break
  print('%s' % (mirror.uri))
  count += 1
