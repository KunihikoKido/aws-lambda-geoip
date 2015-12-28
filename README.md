# GeoIP for AWS Lambda

## About GeoIP lambda function
このlambdaファンクションは、IPアドレスから国名や都市名などの情報を取得するためのLambdaファンクションです。IP情報のデータベースは``GeoLite2-City``を使用しています。

#### Runtime
Python 2.7

#### Lambda Hander
lambda_function.lambda_handler

#### Input event

* ``ip_address``: IP v4 フォーマットIPアドレス
* ``lang``: 結果表示言語（``ru``, ``fr``, ``en``, ``de``, ``zh-cn``, ``pt-br``, ``ja``, ``es``）default to ``en``

Input event sample:
```json
{
  "ip_address": ["61.204.31.74", "127.0.0.1"],
  "lang": "ja"
}
```

#### Execution result

* ``ip_address``: 検索対象IPアドレス
* ``found``: 該当したデータがあったかどうか（true | false）
* ``info.continent``: 大陸名
* ``info.country``: 国名
* ``info.subdivision``: 州・県
* ``info.city``: 都市名
* ``info.postal_code``: 郵便番号
* ``info.location``: 緯度経度
* ``info.time_zone``: タイムゾーン


Execution result sample:
```json
{
  "items": [
    {
      "ip_address": "61.204.31.74",
      "found": true,
      "info": {
        "continent": "アジア",
        "country": "日本",
        "subdivision": "千葉県",
        "city": "千葉市",
        "postal_code": "260-0855",
        "location": [35.6047, 140.1233],
        "time_zone": "Asia/Tokyo"
      }
    },
    {
      "ip_address": "127.0.0.1",
      "found": false
    }
  ]
}
```


## Setup on local machine
ローカルでLambda関数を実行するには、最初に以下のステプで環境をセットアップしてください。

```bash
# 1. Clone this repository with lambda function name.
git clone https://github.com/KunihikoKido/aws-lambda-geoip.git geoip

# 2. Create and activate a virtualenv
cd geoip
virtualenv env
source env/bin/activate

# 3. Install python modules for development.
pip install -r requirements/local.txt

# 4. Install python modules and geolite2 db for lambda function.
fab setup
```

## Run lambda function on local machine
ローカルでLambda関数を実行するには、``fab invoke``コマンドを実行します。

```bash
fab invoke
```

#### Custom event
通常はインプットイベントに``event.json``が使用されますが、他のファイルを使用することも可能です。

以下の例は、新たに作成した``custom-event.json``をインプットイベントに指定して実行する例です。

```bash
fab invoke:custom-event.json
```


## Make bundle zip
以下のステップで、AWS Lambda に登録可能な ``lambda_function.zip`` ファイルが作成されます。

```bash
fab makezip
```

※ ZIPファイルは10MB超えるので、S3経由アップロードしてください。

## Update function code on AWS Lambda

```bash
fab aws-updatecode
```

### Custom function name

```bash
fab aws-updatecode:function1
```

## Invoke function on AWS Lambda

```bash
fab aws-invoke
```

### Custom function name

```bash
fab aws-invoke:function1
```

## Get function configuration on AWS Lambda

```bash
fab aws-getconfig
```

## Snapshot Builds
ビルド済みの``lambda_function.zip``は以下のURLを参照してください。

https://github.com/KunihikoKido/aws-lambda-geoip/releases

## with Amazon API Gateway
### _Example Settings_

_Method and Resources:_

```
GET /geoip
```

_Query Strings:_
* ``ip``: IPアドレス
* ``lang``: 結果表示言語

_Request mapping template:_
```json
{
  "ip_address": ["$util.urlDecode($input.params('ip'))"],
  "lang": "$util.urlDecode($input.params('lang'))"
}
```

_Example Request:_
```bash
GET /geoip?ip=61.204.31.74&lang=ja
```
