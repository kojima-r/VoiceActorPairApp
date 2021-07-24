#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import re
sparql = SPARQLWrapper("http://ja.dbpedia.org/sparql")

q_full="""
SELECT DISTINCT ?name ?animes
WHERE {
  ?ln dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/Category:声優> .
  <http://ja.dbpedia.org/resource/%s> dbo:occupation ?ln .
  ?name dbo:occupation ?ln .
  ?animes dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/%s> .
  ?animes dbo:wikiPageWikiLink ?name .
  ?animes ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
}
"""
q_find_co="""
SELECT DISTINCT ?name
WHERE {
  ?ln dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/Category:声優> .
  <http://ja.dbpedia.org/resource/%s> dbo:occupation ?ln .
  $name dbo:occupation ?ln .
  ?animes dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/%s> .
  ?animes dbo:wikiPageWikiLink $name .
  ?animes ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
}
"""
q_find_anime="""
SELECT DISTINCT ?animes
WHERE {
  ?ln dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/Category:声優> .
  <http://ja.dbpedia.org/resource/%s> dbo:occupation ?ln .
  ?animes dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/%s> .
  ?animes ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
}
"""

q_pair="""
SELECT DISTINCT ?animes
WHERE {
  ?ln dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/Category:声優> .
  <http://ja.dbpedia.org/resource/%s> dbo:occupation ?ln .
  <http://ja.dbpedia.org/resource/%s> dbo:occupation ?ln .
  ?animes dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/%s> .
  ?animes dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/%s> .
  ?animes ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
}
"""
q_va_list="""
SELECT DISTINCT ?name
WHERE {
  ?ln dbo:wikiPageWikiLink <http://ja.dbpedia.org/resource/Category:声優>.
  ?name dbo:occupation ?ln
}
"""
def query_pair(p1,p2):
	#p1="小倉唯"
	#p2="石原夏織"
	sparql.setQuery(q_pair%(p1,p2,p1,p2))
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	data=[]
	anime_list=[]
	for result in results["results"]["bindings"]:
		data.append(dict(result))
		#if "name" in result:
		#	print(re.sub(r'^http://ja\.dbpedia\.org/resource/','',result["name"]["value"]))
		if "animes" in result:
			title=re.sub(r'^http://ja\.dbpedia\.org/resource/','',result["animes"]["value"])
			anime_list.append({"title":title})
	return anime_list

#p1="小倉唯"
#sparql.setQuery(q_find_anime%(p1,p1))


#p1="小倉唯"
#sparql.setQuery(q_find_co%(p1,p1))

#text = json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2)
#with open("data.json", "w") as fh:
    #fh.write(text.encode("utf-8"))
#    fh.write(text)

def make_va_list():
	#p1="小倉唯"
	#p2="石原夏織"
	sparql.setQuery(q_va_list)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	va_list=[]
	for result in results["results"]["bindings"]:
		if "name" in result:
			va=re.sub(r'^http://ja\.dbpedia\.org/resource/','',result["name"]["value"])
			va_list.append({"name":va})
	return va_list

if __name__ == '__main__':
	va_list=make_va_list()
	text = json.dumps(va_list, sort_keys=True, ensure_ascii=False, indent=2)
	with open("va_list.json", "w") as fh:
		#fh.write(text.encode("utf-8"))
		fh.write(text)
	
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
		


