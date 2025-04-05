# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, Response
from co_starring import query_pair
from co_starring import query_pair_entity
import json
import random
app = Flask(__name__)
app.json.ensure_ascii = False # 日本語のため

fp = open('data.json', 'r')
data_list = list(json.load(fp))
fp.close
fp = open('va_list.json', 'r')
va_list = list(json.load(fp))
fp.close
fp = open('anime_list.json', 'r')
anime_list = list(json.load(fp))
fp.close
fp = open('tremor.json', 'r')
tremor_mapping = json.load(fp)
fp.close


print(tremor_mapping)

def jsonp(data, callback="function"):
    return Response(
        "%s(%s);" %(callback, json.dumps(data)),
        mimetype="text/javascript")


@app.route('/')
def index():
    title = "ようこそ"
    print(request.args)
    result={"title":title,"name":"aaa"}
    return jsonify(ResultSet=result)

@app.route('/va_list', methods=['GET', 'POST'])
def get_va_list():
    #name=request.args["name"]
    #result={"title":title,"name":name}
    return jsonify(ResultSet=va_list)

@app.route('/anime_list', methods=['GET', 'POST'])
def get_anime_list():
    #name=request.args["name"]
    #result={"title":title,"name":name}
    return jsonify(ResultSet=anime_list)

@app.route('/random_pair', methods=['GET', 'POST'])
def random_pair():
    pair=random.choice(data_list)
    h="http://ja.dbpedia.org/resource/"
    name1=pair["name1"]["value"][len(h):]
    name2=pair["name2"]["value"][len(h):]
    anime_list=query_pair(name1,name2)
    #print(anime_list)
    result={"query":"pair",
        "name1":name1,
        "name2":name2,
        "anime_list":anime_list}
    callback = request.args.get("callback")
    if callback:
        return jsonp(result, callback)
    return jsonp(result)



@app.route('/pair', methods=['GET', 'POST'])
def pair():
    name1=request.args["name1"]
    name2=request.args["name2"]
    if name1 in tremor_mapping:
        name1=tremor_mapping[name1]
    if name2 in tremor_mapping:
        name2=tremor_mapping[name2]
    anime_list=query_pair(name1,name2)
    result={"query":"pair",
        "name1":name1,
        "name2":name2,
        "anime_list":anime_list}
    callback = request.args.get("callback")
    if callback:
        return jsonp(result, callback)
    return jsonp(result)

#    return jsonify(ResultSet=result)

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')

