from machine import Pin
from Buzzer import Buzzer
from ScoreBord import ScoreBord
import utime,random

class ReflexesGame:
    """反応速度を測るゲーム処理クラス"""
    _high_score = 0
    """ 最高得点 """

    _score_updated = False
    """ 最高得点更新フラグ """

    def __init__(self
                 , pin_lightes
                 , pin_buttons
                 , buzzer_l:Buzzer
                 , buzzer_h:Buzzer
                 , score_bord:ScoreBord
                 , order_size:int = 10):
        """初期化

            Aggs:
                pin_lights:  ライト用GPIOピン番号配列
                pin_buttons: ボタン用GPIOピン番号配列
                buzzer_l:    低音ブザー
                buzzer_h:    高音ブザー
                score_bord:  点数表示用ディスプレイ
                order_size:  ゲーム終了までのボタン順の長さ(デフォルト10)
        """
        self._BUTTON_COUNT = len(pin_lightes)
        self._ORDER_LIST_SIZE = order_size
        self._lightes = []
        for light_pin in pin_lightes:
            self._lightes.append(Pin(light_pin, Pin.OUT, Pin.PULL_UP))
        self._buttons = []
        for button_pin in pin_buttons:
            self._buttons.append(Pin(button_pin, Pin.OUT, Pin.PULL_UP))
        self._buzzer_l = buzzer_l
        self._buzzer_h = buzzer_h
        self._score_bord = score_bord

    def initGame(self):
        """ゲーム初期化
        
            ゲーム中のボタン順をランダムで生成する。
            (同一ボタンが連続で設定されないように調整済)
        """
        order_list = []
        for order_idx in range(self._ORDER_LIST_SIZE):
            target_idx = random.randint(1, self._BUTTON_COUNT) % self._BUTTON_COUNT
            if order_idx > 0:
                if order_list[order_idx - 1] == target_idx:
                    target_idx = (target_idx + 1) % self._BUTTON_COUNT
            order_list.append(target_idx)
        return order_list

    def gameStert(self):
        """ゲーム開始"""
        print("Game Start!")
        self._score_updated = False
        score = 9999
        order_idx = 0
        while score >= 0:
            self._score_bord.output(score)

            # ゲーム終了判定
            if order_idx >= self._ORDER_LIST_SIZE:
                self._gameFinish(score)
                return
            score -= 1
            utime.sleep_ms(1)
        # タイムオーバー処理
        self._timeOver(order_idx)

    def _gameFinish(self, score:int):
        """ゲーム終了"""
        self._score_bord.output(score)
        self._buzzer_l.beep()
        self._buzzer_h.beep()
        if score > self._high_score:
            self._high_score = score
            self._score_updated = True

    def _timeOver(self, order_idx:int):
        """時間切れゲームオーバー処理

        Args:
            order_idx: 現在の表示順(何個目まで進んだかを把握)
        """
        print("Time Over! {0:02}".format(self._ORDER_LIST_SIZE - order_idx))

    def getHighScore(self):
        """現在のハイスコア取得"""
        return self._high_score

    def isScoreUpdated(self):
        """直前のゲームでハイスコア更新したかを取得"""
        return self._score_updated

    def _startSignal(self):
        """ゲーム開始時演出"""
        for cnt in range(3):
            print("cnt:{0}".format(3 - cnt))
            self._buzzer_l.beep()
            utime.sleep_ms(800)
        print("go!")
        self._buzzer_h.beep(500)

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test")
    buzzer_l = Buzzer(14)
    buzzer_h = Buzzer(15)
    score_bord = ScoreBord(0, 21, 22)
    # ==================
    # 点灯順番生成
    # ================== 
    c = ReflexesGame([0,1,2,3,4,5]
                     , [0,1,2,3,4,5]
                     , buzzer_l
                     , buzzer_h
                     , score_bord)
    print(c.initGame())
    c = ReflexesGame([0,1,2,3]
                     , [0,1,2,3]
                     , buzzer_l
                     , buzzer_h
                     , score_bord)
    print(c.initGame())
    # ==================
    # ゲーム開始時処理
    # ================== 
    c._startSignal()
