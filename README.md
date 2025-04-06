# VoiceActorPairApp

[日本語DBpedia](https://ja.dbpedia.org/) からアニメに出演している声優に関しての共演作品を検索するサービス

## 概要

声優はDBpediaで以下に当てはまるページを検索しています
```
?name <http://ja.dbpedia.org/property/職業> <http://ja.dbpedia.org/resource/声優>
```

アニメはDBpediaで以下に当てはまるページを検索しています
```
?animes ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>
```

2025/04/05検索時ではそれぞれのヒット件数は以下の通り
```
voice actor list: 5181
anime list: 3955
```

共演の検索
```
  ?name1 <http://ja.dbpedia.org/property/職業> <http://ja.dbpedia.org/resource/声優>.
  ?name2 <http://ja.dbpedia.org/property/職業> <http://ja.dbpedia.org/resource/声優>.
  ?name1 ?link ?anime.
  ?name2 ?link ?anime.
  ?anime ?p <http://ja.dbpedia.org/resource/プロジェクト:アニメ>.
```
広く検索するために同じアニメのwikipediaページと何らかの関係が張られているというだけで検索にヒットするようにしています


## API

#### `/pair`
`name1`, `name2`のペアから共演作品`anime_list`を検索して返します

#### `/random`
ランダムに`name1`, `name2`, `anime_list`を検索して返します

#### `/anime_list`
登録されているアニメリスト

#### `/va_list`
登録されている声優

