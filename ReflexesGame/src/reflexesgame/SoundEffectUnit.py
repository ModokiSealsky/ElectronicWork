import time
import _thread


class SoundEffectUnit:
    """効果音再生ユニット"""

    def ng(self):
        """お手付き音"""
        # カウントダウンを止めないためにスレッド使用
        _thread.start_new_thread(self.__ng, ())

    def __ng(self):
        """お手付き音"""
        print("ng")

    def ok(self):
        """正解音"""
        print("ok")

    def highscore(self):
        """ハイスコア更新メロディ"""
        print("highscore")

    def gameclear(self):
        """ゲームクリアメロディ"""
        print("gameclear")

    def gameover(self):
        """ゲームオーバーメロディ"""
        print("gameover")

    def pickup(self):
        """点灯音"""
        print("pickup")

    def gamestart(self):
        """ゲーム開始メロディ"""
        print("gamestart")

    def signal_ready(self):
        """信号機カウントダウン音"""
        print("signal_ready")

    def signal_go(self):
        """信号機GO音"""
        print("signal_go")

    def check(self):
        """確認"""
        print("check")


class SoundEffectUnitTester:
    """効果音再生ユニットテスタークラス"""

    def __init__(self, se_unit: SoundEffectUnit):
        self.__se_unit = se_unit

    def test(self):
        print("exec check")
        self.__se_unit.check()
        time.sleep(1)
        print("exec ng thread")
        # スレッドを利用するため、連打の確認
        for roop_cnt in range(3):
            self.__se_unit.ng()
            time.sleep(0.03)
        time.sleep(1)
        print("exec ok")
        self.__se_unit.ok()
        time.sleep(1)
        print("exec highscore")
        self.__se_unit.highscore()
        time.sleep(1)
        print("exec gameclear")
        self.__se_unit.gameclear()
        time.sleep(1)
        print("exec gameover")
        self.__se_unit.gameover()
        time.sleep(1)
        print("exec pickup")
        self.__se_unit.pickup()
        time.sleep(1)
        print("exec gamestart")
        self.__se_unit.gamestart()
        time.sleep(1)
        print("exec signal_ready")
        self.__se_unit.signal_ready()
        time.sleep(1)
        print("exec signal_go")
        self.__se_unit.signal_go()


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    se_unit = SoundEffectUnit()
    tester = SoundEffectUnitTester(se_unit)
    tester.test()
    print("test end   ----")
