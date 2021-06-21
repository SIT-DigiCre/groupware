# データベースについて
本番環境にはMariaDBを、デバッグ環境ではSQLiteを利用しています。  
環境情報は、`.conf/docker.env`の`DEBUG`を`True`もしくは`False`に変更することで設定してください。

## スキーマの管理
スキーマはDjangoのマイグレーション機能を利用しています。  
スキーマファイルは、各ディレクトリ内部の`migrations`ディレクトリ内部に格納されています。

## Dockerコンテナ内部のSQLiteにアクセスする方法
```bash
docker exec -it groupware_db_1 /bin/sh
```

```bash
apt update
apt install -y sqlite3
sqlite3 db.sqlite3
```

## Dockerコンテナ内部のMariaDBにアクセスする方法
```bash
docker exec -it groupware_db_1 /bin/sh
```

```bash
mysql -u ${ユーザ名} -p ${データベース名}
```