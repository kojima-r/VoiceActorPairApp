#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from SPARQLWrapper import SPARQLWrapper, JSON
import json
sparql = SPARQLWrapper("http://ja.dbpedia.org/sparql")
sparql.setQuery("""
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?name ?animes
WHERE {
  ?ln dbpedia-owl:wikiPageWikiLink <http://ja.dbpedia.org/resource/Category:声優> .
  ?name dbpedia-owl:occupation ?ln .
  ?animes dbpedia-owl:wikiPageWikiLink ?name .
  ?animes ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
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


