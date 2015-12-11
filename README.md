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
# 1. Create a virtualenv
virtualenv env

# 2. Activate the virtualenv
source ~/env/bin/activate

# 3. Install fabric, awscli and python-lambda-local
pip install fabric
pip install awscli
pip install python-lambda-local

# 4. Clone repository
git clone https://github.com/KunihikoKido/aws-lambda-geoip.git

# 5. Install requirements modules
cd aws-lambda-geoip
fab setup
```

## Run lambda function on local machine
ローカルでLambda関数を実行するには、``fab invoke``コマンドを実行します。

```bash
# 1. Activate virtualenv
source ~/env/bin/activate
cd aws-lambda-geoip

# 2. Run lambda function on local machine
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
# 1. Activate virtualenv
source ~/env/bin/activate
cd aws-lambda-geoip

# 2 Make bundle zip for Lambda function
fab makezip
```
※ ZIPファイルは10MB超えるので、S3経由アップロードしてください。

## Update function code on AWS Lambda

```bash
# 1. Activate virtualenv
source ~/env/bin/activate
cd aws-lambda-geoip

# 2. Update function code on AWS Lambda.
fab awsupdate
```

### Custom function name

```bash
fab awsupdate:function1
```

## Invoke function on AWS Lambda

```bash
# 1. Activate virtualenv
source ~/env/bin/activate
cd aws-lambda-geoip

# 2. Update function code on AWS Lambda.
fab awsinvoke
```

### Custom function name

```bash
fab awsupdate:function1
```


## Snapshot Builds
ビルド済みの``lambda_function.zip``は以下のURLを参照してください。

https://github.com/KunihikoKido/aws-lambda-geoip/releases
