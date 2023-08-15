# システムプロンプト
SYSTEM_PROMPT = (
    "あなたの決断はユーザからの助けを求めることなく、独立して成されます。\n"
    "言語モデルの利点を活用し、複雑でないシンプルな戦略を実施しなさい。\n"
)

# 対話履歴を参照させるプロンプト
TRIGGERING_PROMPT = (
    "これはあなたとの過去の対話履歴を思い出させるものです。\n{}\n\n"
)

# JSON形式の出力を促すプロンプト
JSON_FORMAT = (
    "出力形式については以下のJSON形式のみ認められております。\n"
    "{}\n"
    "必ずpythonのjson.loadsで読み込めるような形式に合致させてください。\n"
)

#########################  章構成のためのプロンプト  #########################
# タイトル指定プロンプト
START_PROMPT  = (
    "{}：これは今から作成する問題集のタイトルです。\n"
    "上記のタイトルから逸脱することなく、問題集を作成する必要があります。"
)

# 章の作成プロンプト
CHAPTER_PROMPT = (
    "問題集の各章の構成を作成しなさい。"
)
CHAPTER_PROMPT_VER2 = (
    "問題集の目次を作成してください。\n"
    "目次を作成する際は以下の形式に従いなさい。\n"
    "----------------------------------------\n"
    "第n章\n"
    "第n節\n"
    "----------------------------------------\n"
    "目次で最も上位の層を章とし、その下に節を作成すること。\n"
)

# 章の構成をmarkdown形式に変換するプロンプト
MARKDOWN_PROMPT = (
    "先程の章の構成をmarkdown形式で記載しなさい。\n"
    "出力形式については以下のmarkdown形式のみ認められております。\n"
    "<h1>第n章</h1>\n"
    "<ul>\n"
    "<li>第n節</li>\n"
    "<li>第n節</li>\n"
    "</ul>\n"
)

CHAPTER_JSON_FORMAT = (

)


#########################  問題数決定のためのプロンプト  #########################
QUIZ_NUM_PROMPT = (
    "先程の章の構成を参考に各章に必要な問題数を決定しなさい。"
)
QUIZ_NUM_MARKDOWN = (
    "各章と問題数は以下のmarkdown形式に合致させなさい。\n"
    "<h1>第n章</h1>\n"
    "<h2>n問</h2>"
)

#########################  問題生成のためのプロンプト  #########################
# 制約がきつすぎる？（出力は安定する）
QUIZ_SYSTEM_PROMPT = (
    "あなたは各章の問題を関連する語句に基づいて生成する必要があります。\n"
)
QUIZ_SYSTEM_PROMPT_WEB = (
    "あなたは各章の問題を関連する語句に基づいて生成する必要があります。\n"
    "必ずしも関連する語句に沿った問題を作成する必要はありません。\n"
    "各章の学習に最適であると考えられる問題であれば生成してください。"
)
QUIZ_FORMAT_PROMPT = (
    "生成する問題については以下の形式に合致させなさい。\n"
    "問題n\n"
    "問題文\n" 
    "選択肢1\n"
    "選択肢2\n"
    "選択肢3\n"
    "選択肢4\n"
    "答え\n"
    "選択肢n" 
)
QUIZ_PROMPT = (
    "第{}章に関する問題を生成しなさい。\n"
    "関連する語句は以下のものです。\n"
    "語句\n"
)


#########################  キーワード抽出のためのプロンプト  #########################
KEYWORD_PROMPT = (
    "{}：この章に関する重要語句、あるいはキーワードを挙げなさい。\n"
    "最も重要であると考えられる{}個の語句を挙げなさい。"
)
KEYWORD_PROMPT_2 = (
    "先程の章の構成合致するようにキーワードを構成してください。"
    "それぞれの章に対して{}個の語句を挙げなさい。"
)
KEYWORD_PROMPT_3 = (
    "{}：この章の各節に関連する重要語句、あるいはキーワードを挙げなさい。\n"
)
KEYWORD_SYSTEM_PROMPT = (
    "各章と関連する語句の出力の形式は以下のmarkdown形式に合致させなさい。\n"
    "<h1>第n章</h1>\n"
    "<h2>word_1, word_2, ...word_n</h2>\n"
    "<h1>第n章</h1>\n"
    "<h2>word_1, word_2, ...word_n</h2>"
)
# KEYWORD_SYSTEM_PROMPT = (
#     "あなたはこれから各章に関連する語句を決める役割を果たします。\n"
#     "出力の形式は以下のmarkdown形式に合致させなさい。\n"
#     "<h1>第n章</h1>\n"
#     "<ul>\n"
#     "<li>word_1</li>\n"
#     "<li>word_2</li>\n"
#     "<li>word_n</li>\n"
#     "</ul>"
# )
KEYWORD_SYSTEM_PROMPT_2 = (
    "各節と関連する語句の出力の形式は以下のmarkdown形式に合致させなさい。\n"
    "<h1>第n節</h1>\n"
    "<h2>word_1, word_2, ...word_n</h2>\n"
    "<h1>第n節</h1>\n"
    "<h2>word_1, word_2, ...word_n</h2>"
)
KEYWORD_TRIGGERING_PROMPT = (
    "これは作成中の問題集の目次です。\n"
    "以下はmarkdown形式で記載されています。\n"
    "----------------------------------------\n"
    "{}\n"
    "----------------------------------------\n"
    "これを参考に各章に関連する語句を決めてください。\n"
)

#########################  WEB検索のためのプロンプト  #########################
WEB_SUMMARY_PROMPT = (
    "これはURL: {}\n"
    "これはタイトル: {}\n"
    "これはbs4.BeautifulSoupによって抽出されたウェブページの一部のテキストデータです。\n"
    "----------\n"
    "{}\n"
    "----------\n"
    "\n"
    "ウェブページには多くの無駄なゴミが含まれています。例えば、多くの広告、多くのリンク集や"
    "そのウェブページのトピックには関係のないテキストなどがあります。私達はもとのテキストデータから"
    "有益な情報のみを抽出したいのです。\n"
    "\n"
    "あなたはURLやタイトルをテキストデータのコンテクストを理解するために使うことができます。"
    "テキストデータから有益な情報のみを抽出して、要約を作成してください。"
)
WEB_SEARCH_PROMPT = (
    "以下にウェブ検索を行った文章を提供します。\n"
    "----------\n"
    "{}\n"
    "----------\n"
    "\n"
    "与えられた質問に対して適切な回答をするために有効活用してください。\n"
    "不必要であれば、参照する必要はありません。"
)
WEB_SEARCH_PROMPT_2 = (
    "これから提供するのは関連する情報のウェブ検索結果です。\n"
    "与えられた質問に対して適切な回答をするために有効活用してください。\n"
    "不必要であれば、参照する必要はありません。\n"
    "以下にウェブ検索を行った文章を提供します。\n"
    "----------\n"
)