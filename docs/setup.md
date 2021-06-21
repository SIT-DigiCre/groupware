# サーバの起動方法
本アプリケーションは、ローカルでの起動とDockerコンテナ内での起動が可能です。環境情報を統一するため、Dockerコンテナ内での起動を推奨します。**どちらの起動方法を利用する場合も下記の共通手順を必ず実施してください。**

起動後、`http://localhost:80/`でアクセス出来れば正常に起動できています。

## 共通手順
共通手順は2つです。

1. アプリケーションの設定ファイルである、 `.conf/docker.env.sample` を `.conf/docker.env` にコピーしてください
2. `digigru/`ディレクトリ下に、`local_settings.py`というファイルを作成し、下記の通り`SECRET_KEY`および`EMAIL_HOST_PASSWORD`を設定してください

```python
# ./digigru/local_settings.py
SECRET_KEY='SUPER_STRONG_PASSWORD' # ./digigru/get_random_secret_key.pyで生成してください
EMAIL_HOST_PASSWORD='SUPER_STRONG_PASSWORD' # 管理者から受け取ってください
```

## ローカルで起動する
ローカルでアプリケーションを起動して、そこにローカルから接続します。

下記のコマンドはLinux用です。Windowsで利用する場合は、適宜読みかえてください。よく分からない場合は、管理者に確認してください。

1. 必要なツールをインストールする

```bash
sudo apt update
sudo apt install -y python3-dev libffi-dev build-essential virtualenvwrapper
exec $SHELL -l # terminalの再起動(exitで一度閉じても良い)
```

2. 仮想環境の構築
```bash
mkvirtualenv --python=$(which python3) groupware
```

3. Pythonのパッケージ(ライブラリ)の一括インストール
```bash
pip install -r requirements.txt
```

## Dockerコンテナ内で起動する
Docker-Composeを用いて、Dockerコンテナ内部でアプリケーション、DB、Nginxを起動します。Dockerのインストールは[こちら](https://docs.docker.com/get-docker/)、Docker-Composeのインストールは[こちら](https://docs.docker.com/compose/install/)を参考にしてください。

起動時は下記のコマンドを実行してください。

```bash
docker-compose up --build -d # --buildオプションや-dオプションは適宜付けたり付けなかったりしてください
```

終了時は下記のコマンドを実行してください。

```bash
docker-compose down
```
