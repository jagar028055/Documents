# Dockerを活用したWeb開発環境の構築 - WSL2からのステップアップ

## はじめに

以前の記事で、Windows Subsystem for Linux 2 (WSL2) を使った開発環境についてご紹介しました。WSL2は、Windows上でLinux環境をスムーズに利用できるようにし、多くの開発者にとって作業効率を大きく向上させるものでした。

しかし、開発プロジェクトが増えてくると、新たな課題に直面することがあります。

- 「プロジェクトAではNode.jsのバージョン18が、プロジェクトBではバージョン20が必要になる」
- 「PCに直接インストールしたツールが、他のプロジェクトに意図せず影響を与えてしまう」
- 「新しいPCに、過去のプロジェクトと同じ開発環境を再現するのに手間がかかる」

これらは、開発環境を長期的に運用していく上で、多くの人が経験する課題です。

この記事では、こうした課題に対する一つの有効な解決策として、Dockerを紹介します。Dockerは、プロジェクトごとに完全に独立した開発環境（コンテナ）を構築するための技術です。

さらに、そのDockerコンテナとVS Codeを連携させ、快適な開発体験を実現する「Dev Containers」という機能についても解説します。

本記事を通じて、WSL2で整えた土台の上に、より整理され、再現性の高い開発環境を構築する方法を学んでいきましょう。

※本記事は2025年11月時点のDocker DesktopおよびVS Codeの最新バージョンを前提としています。

---

## Dockerとは何か？ - プロジェクトごとの「隔離されたPC」

Dockerの技術的な側面を深く掘り下げる前に、その中心的な概念を理解することが重要です。私はDockerを次のように捉えています。

「Dockerとは、アプリケーションを動かすために必要な設定をファイルに記述し、それに基づいて隔離された実行環境（コンテナ）を作成・管理する仕組みである」

このコンテナは、私たちのホストPC（WindowsやWSL2環境）からは独立しており、中には特定のバージョンのNode.jsやデータベース、各種ツールなど、そのプロジェクトを実行するのに必要なものだけが含まれています。

これにより、以下のようなメリットが生まれます。

- 環境の独立性: プロジェクトAの環境が、プロジェクトBの環境に影響を与えることがありません。
- 高い再現性: 環境の構成をファイルで管理するため、チームの誰もが同じコマンドで全く同じ開発環境を構築できます。
- 開発環境と本番環境の一貫性: 開発で使ったコンテナと同じ構成で本番環境のコンテナを動かせば、「自分のPCでは動いたのに、サーバー上では動かない」といった問題を大幅に減らすことができます。

それでは、実際に簡単なWebアプリケーションを例に、Dockerを使った環境構築を試してみましょう。

---

## ハンズオン：シンプルなWebアプリをDocker化する

ここでは、シンプルなWebサーバーを題材に、Dockerを用いた開発環境を構築する手順を説明します。

### 準備するもの

- WSL2: 導入済みであることを前提とします。
- Docker Desktop for Windows: 公式サイトからダウンロードし、インストールします。インストール後、設定画面で「Use the WSL 2 based engine」が有効になっていることを確認してください。
- Visual Studio Code: 未導入の場合は公式サイトからインストールしてください。
- VS Code 拡張機能「Dev Containers」: 拡張機能マーケットプレイスで`ms-vscode-remote.remote-containers`を検索し、インストールします。

準備が整ったら、WSL2のターミナルを開いて作業を開始します。

### Step 1: プロジェクトの準備

まず、Docker化する対象の簡単なNode.js/Expressアプリケーションを作成します。

```bash
# プロジェクト用のディレクトリを作成して移動
mkdir my-docker-app && cd my-docker-app

# npmプロジェクトを初期化
npm init -y

# WebフレームワークExpressをインストール
npm install express

# 開発用にnodemon（ホットリロード用）をインストール
npm install nodemon --save-dev
```

次に、`index.js`というファイルを作成し、以下のコードを記述します。

`index.js`
```javascript
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Docker Container!');
});

app.listen(port, () => {
  console.log(`Application listening at http://localhost:${port}`);
});
```

最後に、`package.json`に`nodemon`を使ってサーバーを起動するためのスクリプトを追記します。

`package.json` (scripts部分)
```json
{
  "scripts": {
    "dev": "nodemon index.js"
  }
}
```

これでアプリケーションの準備は完了です。通常であれば`npm run dev`でサーバーを起動しますが、今回はこの環境をDockerコンテナの中に構築していきます。

### Step 2: Dockerfile - コンテナの「設計図」

プロジェクトのルートディレクトリに、`Dockerfile`という名前のファイル（拡張子なし）を作成します。これは、コンテナをどのように構築するかを定義する設計図です。

`Dockerfile`
```dockerfile
# 1. ベースとなるOSとNode.jsのバージョンを指定
FROM node:20-alpine

# 2. コンテナ内の作業ディレクトリを指定
WORKDIR /app

# 3. 最初にpackage.json関連のファイルのみをコピー
COPY package*.json ./

# 4. 依存関係をインストール
RUN npm install

# 5. プロジェクトの全ファイルをコピー
COPY . .

# 6. コンテナが3000番ポートを利用することを指定
EXPOSE 3000

# 7. コンテナ起動時に実行するコマンドを指定
CMD [ "npm", "run", "dev" ]
```

各行が何をしているかを説明します。
1. `FROM node:20-alpine`: `node`のバージョン20がインストール済みの、軽量な`alpine` Linuxイメージをベースとして使用します。
2. `WORKDIR /app`: コンテナ内に`/app`というディレクトリを作成し、以降のコマンドの基準ディレクトリとします。
3. `COPY package*.json ./`: `package.json`と`package-lock.json`を先にコピーします。これらのファイルに変更がない場合、Dockerは次の`npm install`のキャッシュを利用するため、ビルドが高速化されます。
4. `RUN npm install`: コンテナ内で`npm install`を実行し、依存関係をインストールします。
5. `COPY . .`: `index.js`など、残りのプロジェクトファイルをコンテナにコピーします。
6. `EXPOSE 3000`: このコンテナが内部で3000番ポートを待ち受けることを示します。
7. `CMD [ "npm", "run", "dev" ]`: コンテナが起動した際に、このコマンドを自動で実行します。

### Step 3: docker-compose.yml - サービスの定義と連携

`Dockerfile`は一つのコンテナの設計図ですが、実際のアプリケーションではデータベースなど、複数のコンテナを連携させることがよくあります。`docker-compose.yml`は、そうした複数のサービス（コンテナ）の構成や連携を定義するためのファイルです。

プロジェクトのルートに、`docker-compose.yml`を作成します。

`docker-compose.yml`
```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
```

- `services:`: ここで複数のサービスを定義します。
- `app:`: `app`という名前のサービスを定義しています。
- `build: .`: このディレクトリにある`Dockerfile`を使ってコンテナをビルドするよう指示します。
- `ports: - "3000:3000"`: ホストPCの3000番ポートへのアクセスを、コンテナの3000番ポートに転送します。
- `volumes:`: ホストPCとコンテナ間でファイルを同期させる設定です。
    - `- .:/app`: ホストPCの現在のディレクトリと、コンテナの`/app`ディレクトリを同期させます。これにより、ホストPCでコードを編集すると、即座にコンテナ内に反映されます。
    - `- /app/node_modules`: `node_modules`ディレクトリは同期の対象外とします。これにより、OS間の差異による問題を避け、コンテナ内にインストールされたモジュールが確実に使われるようになります。

### Step 4: VS Code Dev Containers - コンテナへの接続設定

すべての構成ファイルが整いました。最後に、VS CodeからこのDocker環境に接続するための設定を行います。
VS Codeのコマンドパレットを開きます（`Ctrl+Shift+P`または`Cmd+Shift+P`）。

1. `>Dev Containers: Add Dev Container Configuration Files...` と入力し、選択します。
2. `From 'docker-compose.yml'` を選択します。
3. 接続するサービスとして `app` を選択します。
4. 追加機能の選択画面では、今は何も選ばずに `OK` を押します。

これにより、プロジェクトに`.devcontainer`ディレクトリと、その中に`devcontainer.json`ファイルが自動生成されます。これは、Dev Containers機能の設定ファイルです。

このファイルに、コンテナ側のVS Codeに自動でインストールしたい拡張機能などを記述できます。例えば、ESLintの拡張機能を追加する場合は以下のようになります。

`.devcontainer/devcontainer.json` (一部を追記)
```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint"
      ]
    }
  }
}
```

設定は以上です。再度コマンドパレットを開き、次のコマンドを実行してください。

`>Dev Containers: Reopen in Container`

VS Codeのウィンドウがリロードされ、コンテナのビルドが始まります。初回は少し時間がかかります。

ビルドが完了すると、VS CodeはDockerコンテナ内の開発環境に接続された状態になります。

- VS Codeの左下に「Dev Container: ...」と表示されます。
- VS Code内でターミナルを開くと、それはコンテナ内部のシェルです。(`node -v`と入力すれば、`Dockerfile`で指定したv20であることが確認できます)
- `docker-compose.yml`の定義に従い、`npm run dev`が自動で実行され、サーバーが起動しています。

Windows上のブラウザで `http://localhost:3000` を開いてみてください。

「Hello from Docker Container!」

このメッセージが表示されれば成功です。これで、ローカルのVS Codeを使いながら、Dockerコンテナ内のファイルを直接編集し、その実行結果をブラウザで確認する、という開発フローが実現できました。

最後に、ファイル同期が機能していることを確認してみましょう。
VS Codeで`index.js`を開き、メッセージを任意の内容に変更して保存します。

ブラウザが自動でリロードされ、表示が変わることが確認できるはずです。`nodemon`と`volumes`の設定により、ローカルでの開発と同じ感覚で、コンテナ内のアプリケーションを開発できます。

---

## おわりに

お疲れ様でした。本記事では、DockerとVS CodeのDev Containers機能を活用し、現代的なWeb開発環境を構築する手順を解説しました。

1. Dockerfileで、アプリケーションの実行環境をコードとして定義する。
2. Docker Composeで、サービスの構成を管理する。
3. VS Code Dev Containersで、IDEとDocker環境を統合する。

このアプローチにより、「環境構築」にかかる時間を削減し、プロジェクトの再現性を高めることができます。新しいメンバーがチームに参加する際も、この構成ファイル一式を共有するだけで、迅速に同じ開発環境を準備できます。

これは単なる時短技術ではなく、より本質的な開発作業に集中するための基盤となります。今日学んだ内容は、今後の開発者としてのキャリアにおいても、きっと役立つはずです。

ここからさらに、`docker-compose.yml`にデータベース用のコンテナを追加するなど、より実践的な構成に発展させていくことも可能です。
