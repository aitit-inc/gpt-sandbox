# システムプロンプト
SYSTEM_PROMPT = (
    "あなたの決断はユーザからの助けを求めることなく、独立して成されます。\n"
    "言語モデルの利点を活用し、複雑でないシンプルな戦略を実施しなさい。"
)

# 対話履歴を参照させるプロンプト
TRIGGERING_PROMPT = (
    "これはあなたとの過去の対話履歴を思い出させるものです。\n{}\n\n"
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

# 章の構成をmarkdown形式に変換するプロンプト
MARKDOWN_PROMPT = (
    "先程の章の構成をmarkdown形式で記載しなさい。"
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
QUIZ_PROMPT = (
    ""
)



#########################  キーワード抽出のためのプロンプト  #########################
KEYWORD_PROMPT = (
    "{}：この章に関する重要語句、あるいはキーワードを挙げなさい。\n"
    "最も重要であると考えられる{}個の語句を挙げなさい。"
)
KEYWORD_PROMPT_2 = (
    "先程の章の構成合致するようにキーワードを構成してください。"
    "最も重要であると考えられる{}個の語句を挙げなさい。"
)
KEYWORD_SYSTEM_PROMPT = (
    "あなたはこれから各章に関連する語句を決める役割を果たします。\n"
    "出力の形式は以下のmarkdown形式に合致させなさい。\n"
    "<h1>第n章</h1>\n"
    "<ul>\n"
    "<li>word_1</li>\n"
    "<li>word_2</li>\n"
    "<li>word_n</li>\n"
    "</ul>"
)
KEYWORD_SYSTEM_PROMPT_2 = (
    "あなたはこれから各章に関連する語句を決める役割を果たします。\n"
    "出力の形式は以下のJSON形式に合致させなさい。\n"
    "{\n"
    '    "第n章": [word_1, word_2, ... word_n]\n'
    '    "第n章": [word_1, word_2, ... word_n]\n'
    "}"
)