import urllib.request
from bs4 import BeautifulSoup, Tag
import sys
import json
import IPython

url = "https://www.morebeer.com/articles/homebrew_beer_hops"
with urllib.request.urlopen(url) as fp:
  soup = BeautifulSoup(fp.read().decode("utf8"), features="lxml")

hops = {}
def publish(l):
  name = str.strip(l[0].text)
  if len(name) == 0:
    return
  desc = ''.join(map(lambda x: str.strip(''.join(x.strings)), l[1:]))
  hops[name] = {
    'name': name,
    'desc': desc
  }

res = soup.find('h3')
current_hop = []
while res:
  current_hop.append(res)
  res = res.find_next_sibling()
  if not res:
      break
  if res.name == 'h3':
      publish(current_hop)
      current_hop = []
  elif res.name == 'h2':
      break

publish(current_hop)

for name, data in hops.items():
  print("{} :\n{}\n{}\n\n".format(name, "-"*(len(name)+2), data["desc"]))

with open('../hops_graph/hops_descriptions.json', 'w') as jsonfile:
  json.dump(hops, jsonfile)