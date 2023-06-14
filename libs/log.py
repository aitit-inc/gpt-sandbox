import logging

# ログメッセージ定義
LOG_START = "処理開始"
LOG_COMPLETE= "処理終了"


def init(level=logging.INFO):
    """
    説明：ログインスタンスの初期化
    引数：ログ出力モード
    戻り値：ログインスタンス
    """
    # ログインスタンス初期化
    logger = logging.getLogger()
    logger.propagate = False
    # ログ出力モード設定
    logger.setLevel(level)
    # 不要ハンドル削除
    while logger.handlers:
        logger.handlers.pop()

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger