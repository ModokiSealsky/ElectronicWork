from machine import Pin
import utime

class JankenVoice:
    def __init(self):
        """コンストラクタ"""

    def callJan(self):
        """「じゃん」を再生する"""
        print("じゃん")

    def callKen(self):
        """「けん」を再生する"""
        print("けん")
    
    def callPon(self):
        """「ぽん」を再生する"""
        print("ぽん")

    def callTimeUp(self):
        """時間切れメッセージを再生する"""
        print("おそい")

    def callWin(self):
        """プレイヤー勝利メッセージを再生する"""
        print("やったね")

    def callLose(self):
        """プレイヤー敗北メッセージを再生する"""
        print("まけた")

    def callDraw(self):
        """あいこメッセージを再生する"""
        print("もう一回")

    def callStart(self):
        """開始メッセージを再生する"""
        print("いくよ")

    def callVictory(self):
        """9勝達成メッセージを再生する"""
        print("おめでとう")


# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start -----")
    clz = JankenVoice()
    clz.callJan()
    clz.callKen()
    clz.callPon()
    clz.callTimeUp()
    clz.callWin()
    clz.callLose()
    clz.callDraw()
    clz.callStart()
    clz.callVictory()
    print("test end   -----")
