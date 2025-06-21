
class JankenVoice:
    """音声再生インターフェース"""

    def __init__(self):
        """コンストラクタ"""

    def call_jan(self):
        """「じゃん」を再生する"""
        print("じゃん")

    def call_ken(self):
        """「けん」を再生する"""
        print("けん")
    
    def call_pon(self):
        """「ぽん」を再生する"""
        print("ぽん")

    def call_timeUp(self):
        """時間切れメッセージを再生する"""
        print("おそい")

    def call_win(self):
        """プレイヤー勝利メッセージを再生する"""
        print("やったね")

    def call_lose(self):
        """プレイヤー敗北メッセージを再生する"""
        print("まけた")

    def call_draw(self):
        """あいこメッセージを再生する"""
        print("もう一回")

    def call_start(self):
        """開始メッセージを再生する"""
        print("いくよ")

    def call_victory(self):
        """9勝達成メッセージを再生する"""
        print("おめでとう")

    def call_gu(self):
        """グー"""
        print("グー")

    def call_ch(self):
        """チョキ"""
        print("チョキ")

    def call_pa(self):
        """パー"""
        print("パー")


# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start -----")
    clz = JankenVoice()
    clz.call_jan()
    clz.call_ken()
    clz.call_pon()
    clz.call_timeUp()
    clz.call_win()
    clz.call_lose()
    clz.call_draw()
    clz.call_start()
    clz.call_victory()
    clz.call_gu()
    clz.call_ch()
    clz.call_pa()
    print("test end   -----")
