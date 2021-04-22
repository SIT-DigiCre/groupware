# DigiCore

![CI](https://github.com/SIT-DigiCre/groupware/workflows/CI/badge.svg)
![CD](https://github.com/SIT-DigiCre/groupware/workflows/CD/badge.svg)

DigiCoreは、[デジクリ](https://digicre.net/)で利用されているグループウェアです。Digicoreを用いることで、アカウントや企画、稟議の管理、掲示板やブログを一括管理することが出来ます。

## 開発環境のセットアップ方法
本アプリケーションは、ローカルでの起動とDockerコンテナ内での起動が可能です。  
実行すべきコマンドや設定方法の詳細は、[setup.md](./docs/setup.md)をご確認ください。  
また、本番環境とデバッグ環境でデータベースが異なります。データベースの詳細については、[database.md](./docs/database.md)をご確認ください。

## アプリケーション構成
本アプリケーションは、Djangoフレームワークを用いたシェアードナッシングアーキテクチャで構成されます。アプリケーションでのデータの流れや各ディレクトリの責務の詳細は、[architecture.md](./docs/architecture.md)をご確認ください。

## ライセンス
本リポジトリのコードは[MITライセンス](./LICENSE)下にあります。
