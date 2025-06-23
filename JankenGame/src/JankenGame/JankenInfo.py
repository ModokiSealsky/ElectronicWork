class JankenInfo:
    def __init__(self):
        """
        Args:

        """

    def output_win_count(self, win_count: int):
        """現在の勝利数を出力する
        Args:
            count: 勝利数
        """
        print("win_count:{0}".format(win_count))

    def output_game_mode(self, mode: str):
        """ゲームモードを出力する"""
        print("mode:{0}".format(mode))

    def output_message(self, message: str):
        """メッセージを出力する"""
        print("message:{0}".format(message))
