import urllib.request
from bs4 import BeautifulSoup
import sys
import json
import IPython

with urllib.request.urlopen("https://www.rolling-beers.fr/fr/content/29-liste-complete-des-houblons") as fp:
  soup = BeautifulSoup(fp.read().decode("utf8"), features="lxml")

a = soup.find(id="listecomplete")

def parse_line_field(x):
  delim = " : "
  l = x.split(delim)
  return l[0], delim.join(l[1:])

def fix_link(x):
  d = { 
    'aucun' : [],
    
    'Challenger Northern Brewer': [ "Northern Brewer" ],
    'Apoll': [ "Apollo" ],
    'Columbus': [ "Columbus / Tomahawk / Zeus (CTZ)" ],
    'Zeus': [ "Columbus / Tomahawk / Zeus (CTZ)" ],
    'Williamette': [ "Willamette" ],
    'Fuggles': [ "Fuggle" ],
    'Hallertauer': [ "Hallertau" ],
    'Hersbruck':   [ "Hallertau Hersbrucker" ],
    'Hersbrucker': [ "Hallertau Hersbrucker" ],
    'Hallertau Mittelfrueh': [ "Hallertau Mittelfrüh" ],
    'Mittlefruh et Amarillo': [ "Hallertau Mittelfrüh", "Amarillo" ],
    'Tettnanger': [ "Tettnang" ],
    'Mont Hood': [ "Mount Hood" ],
    'Pearl': [ "Perle" ],
    'A combination of Columbus and Centennial might come close,': [ "Columbus / Tomahawk / Zeus (CTZ)", "Centennial" ],
    'Styrian Golding': [ "Styrian Goldings" ],
    'Eat Kent Goldings': [ "East Kent Goldings" ],
    'Le Galaxy / Nelson Sauvin allemand': [ "Galaxy", "Nelson Sauvin" ],
    'EKG': [ "East Kent Goldings" ],
    
    'Legacy': [],
    'Mix of English and Noble varieties': []
  }
  return d[x] if x in d else [x]

def parse_hop(p):
  lines = list(filter(lambda x: x, map(lambda x: x.string, p.contents)))
  name = lines[0]
  fields = {}
  fields["name"] = name
  for line in lines[1:]:
    k,v = parse_line_field(line)
    fields[k] = v
  links = []
  if "Similaire à" in fields:
    for x in fields["Similaire à"].split(", "):
      links += fix_link(str.strip(x))
  fields["links"] = links
  return fields

hops = {}
while a.find_next_sibling('p'):
  a = a.find_next_sibling('p')
  hop = parse_hop(a)
  hops[hop["name"]] = hop

missing_hops = set()
for hop_name, hop in hops.items():
  for link in hop["links"]:
    if link not in hops:
      print("Hop '{}' has link '{}' that doesn't exist.".format(hop_name, link))
      missing_hops |= { link }


print("="*20)
print("Known hops:")
for x in list(sorted(hops.keys())):
  print(" - {}".format(x))
print("="*20)
print("Missing hops:")
for x in sorted(list(missing_hops)):
  print(" - {}".format(x))
print("="*20)
print("\n")


#for hop_name, hop in hops.items():
#    for link in hop["links"]:
#      print("{} -> {}".format(hop_name,link))


data = {
  "nodes": [
    {
      "data": {
        "id": hop_name,
        "label": hop_name
      }
    }
    for hop_name, hop in hops.items()
  ],
  "edges": [
    {
      "data": {
        "source": hop_name,
        "target": link
      }
    }
    for hop_name, hop in hops.items()
    for link in hop["links"]
  ]
}
with open('../hops_graph/graph.json', 'w') as jsonfile:
  json.dump(data, jsonfile)