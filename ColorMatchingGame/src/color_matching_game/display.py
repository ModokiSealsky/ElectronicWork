"""表示用クラスパッケージ"""


class ScoreBord:
    """スコアボードクラス"""

    def set_score(self, score: int):
        """スコア設定
        Args:
            score: スコア
        """
        print(f"score:{score}")

    def off(self):
        """消灯"""
        print("score bord off")


class TimeBord:
    """タイムボードクラス"""

    def set_time(self, time: int):
        """タイム設定
        Args:
            time: タイム
        """
        print(f"time:{time}")

    def off(self):
        """消灯"""
        print("score bord off")
