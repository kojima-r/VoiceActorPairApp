#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import re
sparql = SPARQLWrapper("http://ja.dbpedia.org/sparql")

q_pair="""
SELECT DISTINCT ?animes
WHERE {
  <%s> <http://ja.dbpedia.org/property/職業> <http://ja.dbpedia.org/resource/声優>.
  <%s> <http://ja.dbpedia.org/property/職業> <http://ja.dbpedia.org/resource/声優>.
  <%s> ?link1 ?animes.
  <%s> ?link2 ?animes.
  ?animes ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
}
"""

q_va_list="""
SELECT DISTINCT ?name
WHERE {
  ?name <http://ja.dbpedia.org/property/職業> <http://ja.dbpedia.org/resource/声優>.
  ?name ?link ?anime.
  ?anime ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
}
"""
q_anime_list="""
SELECT DISTINCT ?animes
WHERE {
  ?name <http://ja.dbpedia.org/property/職業> <http://ja.dbpedia.org/resource/声優>.
  ?animes ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
  ?name ?link ?animes.
}
"""


def query_pair(p1,p2):
    p1="http://ja.dbpedia.org/resource/"+p1
    p2="http://ja.dbpedia.org/resource/"+p2
    return query_pair_entity(p1,p2)

def query_pair_entity(p1,p2):
    print(q_pair%(p1,p2,p1,p2))
    sparql.setQuery(q_pair%(p1,p2,p1,p2))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data=[]
    anime_list=[]
    for result in results["results"]["bindings"]:
        data.append(dict(result))
        if "animes" in result:
            title=re.sub(r'^http://ja\.dbpedia\.org/resource/','',result["animes"]["value"])
            anime_list.append({"title":title})
    print(len(data))
    return anime_list

def make_va_list():
    sparql.setQuery(q_va_list)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    va_list=[]
    for result in results["results"]["bindings"]:
        if "name" in result:
            va=re.sub(r'^http://ja\.dbpedia\.org/resource/','',result["name"]["value"])
            va_list.append({"name":va})
    return va_list
def make_anime_list():
    sparql.setQuery(q_anime_list)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    anime_list=[]
    for result in results["results"]["bindings"]:
        if "animes" in result:
            anime=re.sub(r'^http://ja\.dbpedia\.org/resource/','',result["animes"]["value"])
            anime_list.append(anime)
    return anime_list


if __name__ == '__main__':
    va_list=make_va_list()
    print("voice actor list:",len(va_list))
    text = json.dumps(va_list, sort_keys=True, ensure_ascii=False, indent=2)
    with open("va_list.json", "w") as fh:
        #fh.write(text.encode("utf-8"))
        fh.write(text)
    anime_list=make_anime_list()
    print("anime list:",len(anime_list))
    text = json.dumps(anime_list, sort_keys=True, ensure_ascii=False, indent=2)
    with open("anime_list.json", "w") as fh:
        #fh.write(text.encode("utf-8"))
        fh.write(text)
    

    ##
    tremor_mapping={}
    for el in va_list:
        name=el["name"]
        tremor=re.sub(r'_\(.*\)',"",name)
        if tremor!=name:
            tremor_mapping[tremor]=name
    print(tremor_mapping)
    text = json.dumps(tremor_mapping, sort_keys=True, ensure_ascii=False, indent=2)
    with open("tremor.json", "w") as fh:
        fh.write(text)
        


