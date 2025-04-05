#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from SPARQLWrapper import SPARQLWrapper, JSON
import json
sparql = SPARQLWrapper("http://ja.dbpedia.org/sparql")
sparql.setQuery("""
SELECT DISTINCT ?name1 ?name2
WHERE {
  ?name1 <http://ja.dbpedia.org/property/職業> <http://ja.dbpedia.org/resource/声優>.
  ?name2 <http://ja.dbpedia.org/property/職業> <http://ja.dbpedia.org/resource/声優>.
  ?name1 ?link ?anime.
  ?name2 ?link ?anime.
  ?anime ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
  FILTER(?name1 < ?name2).
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

data=[]
for result in results["results"]["bindings"]:
    #print(type(result))
    data.append(dict(result))
    #print(dict(result))
print(len(data))
text = json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2)
with open("data.json", "w") as fh:
    #fh.write(text.encode("utf-8"))
    fh.write(text)


