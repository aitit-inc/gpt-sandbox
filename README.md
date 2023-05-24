# LLM PoC Project

大規模言語モデルの活用と技術検証

## Quick Start

### 必須事項

- コマンド

```shell
cd ~./LLM_pj
touch .env
```

- .envファイルの中に

```conf
OPENAI_API_KEY=your_api_key
```

- ライブライのインストール

```shell
pip install --upgrade pip
pip install -r requirements.txt
```

## フォルダ説明

- autogpt_PoC: AutoGPTの検証、調査

- libs: 共通関数ライブラリ

## a. 章立てを生成する

- 主クラス：ChapterCreator（libs/agent.py）

- 実行関数名：create_chapteres

## b. 問題数を決定する

- 主クラス：QuizCreator（libs/agent.py）

- 実行関数名：num_of_quiz

## c. 章ごとにキーワード群を決める

- 主クラス：KeywordCreator（libs/agent.py）

- 実行関数名：get_keywords

## d. 問題を生成する


## テスト実施ファイル（pytest_test.py）

- 実行コマンド

```shell
python pytest_test.py
```

### 説明

- start()：テストの実施関数

- test_func()：章の構成作成機能のテスト関数

- main()：章の構成と各章あたりの問題数を出力する関数