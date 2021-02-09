# DigiCore

## 環境構築

1. Dockerが動く環境を用意する
2. `apt-get install python3-dev libmysqlclient-dev`  
3. `pip3 install -r requirements.txt`

## 設定
次のような設定ファイルを`.conf/docker.env`として追加する。
```
DEBUG=True
MYSQL_ROOT_PASSWORD=digicre
MYSQL_DATABASE=digicre
MYSQL_USER=digicre
MYSQL_PASSWORD=digicre
```
