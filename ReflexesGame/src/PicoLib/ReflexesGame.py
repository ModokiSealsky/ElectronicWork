from .Buzzer import Buzzer
from .InputSwitch import InputSwitch
from .Led import Led
from .ScoreBord import ScoreBord
import utime,random

class ReflexesGame:
    """反応速度を測るゲーム処理クラス"""
    _high_score = 0
    """ 最高得点 """

    _score_updated = False
    """ 最高得点更新フラグ """

    def __init__(self
                 , lightes:list[Led]
                 , buttons:list[InputSwitch]
                 , buzzer_l:Buzzer
                 , buzzer_h:Buzzer
                 , score_bord:ScoreBord
                 , led_highscore:Led
                 , led_timeup:Led
                 , order_size:int = 10):
        """初期化

            Aggs:
                lights:      ライト用LED配列
                buttons:     ボタン配列
                buzzer_l:    低音ブザー
                buzzer_h:    高音ブザー
                score_bord:  点数表示用ディスプレイ
                led_highscore: スコア更新LED
                led_timeup:    時間切れLED
                order_size:  ゲーム終了までのボタン順の長さ(デフォルト10)
        """
        self._BUTTON_COUNT = len(lightes)
        self._ORDER_LIST_SIZE = order_size
        self._lightes = lightes
        self._buttons = buttons
        self._buzzer_l = buzzer_l
        self._buzzer_h = buzzer_h
        self._score_bord = score_bord
        self._led_highscore = led_highscore
        self._led_timeup = led_timeup

    def partsCheck(self):
        """パーツチェック"""
        # ライトチェック
        for l in self._lightes:
            l.on()
        utime.sleep(2)
        for l in self._lightes:
            l.off()
        # 結果ライト、ブザーチェック
        self._led_highscore.on()
        self._buzzer_h.beep()
        utime.sleep(2)
        self._led_timeup.on()
        self._buzzer_l.beep()
        utime.sleep(2)
        # 7セグディスプレイチェック
        self._score_bord.displayCheck()
        # ボタンチェック 2個以上同時押しで終了
        btn_cnt = 0
        while btn_cnt < 2:
            btn_cnt = 0
            for b in self._buttons:
                if b.isOn():
                    self._buzzer_l.beep()
                    btn_cnt += 1

    def _initDisplay(self):
        """表示系初期化"""
        self._led_highscore.off()
        self._led_timeup.off()
        for light_idx in range(self._BUTTON_COUNT):
            self._lightes[light_idx].off()

    def initGame(self, order_list_size:int, button_count:int):
        """ゲーム初期化
        
            ゲーム中のボタン順をランダムで生成する。
            (同一ボタンが連続で設定されないように調整済)

        Args:
            order_list_size:
        """
        order_list:list[int] = []
        for order_idx in range(order_list_size):
            target_idx = random.randint(1, button_count) % button_count
            if order_idx > 0 and order_list[order_idx - 1] == target_idx:
                target_idx = (target_idx + 1) % button_count
            order_list.append(target_idx)
        return order_list

    def gameStert(self):
        """ゲーム開始"""
        print("Game Start!")
        # 初期化
        self._initDisplay()
        self._score_updated = False
        order_list = self.initGame(self._ORDER_LIST_SIZE, self._BUTTON_COUNT)
        order_idx = 0
        now_target = order_list[order_idx]

        # 開始処理
        score = 9999
        self._score_bord.outputScore(score)
        self._score_bord.scoreUpdateThreadStart()
        self._startSignal()
        self._lightOn(now_target)
        while score >= 0:
            self._score_bord.outputScore(score)
            # 正解判定
            if self._isHit(now_target):
                self._lightHit(now_target)
                order_idx += 1
                # ゲーム終了判定
                if order_idx >= self._ORDER_LIST_SIZE:
                    self._gameFinish(score)
                    return
                now_target = order_list[order_idx]
                self._lightOn(now_target)
            score -= 1
            utime.sleep_ms(1)
        # タイムオーバー処理
        self._timeOver(order_idx)

    def _gameFinish(self, score:int):
        """ゲーム終了"""
        self._score_bord.screUpdateThreadStop()
        self._score_bord.outputScore(score)
        self._buzzer_l.beep()
        self._buzzer_h.beep()
        if score > self._high_score:
            self._updateScore(score)

    def _updateScore(self, score:int):
        """ハイスコア更新

        Args:
            score: ゲームスコア
        """
        self._high_score = score
        self._score_updated = True
        self._led_highscore.on()


    def _timeOver(self, order_idx:int):
        """時間切れゲームオーバー処理

        Args:
            order_idx: 現在の表示順(何個目まで進んだかを把握)
        """
        print("Time Over! {0:02}".format(self._ORDER_LIST_SIZE - order_idx))
        self._score_bord.screUpdateThreadStop()
        self._buzzer_l.beep(1000)
        self._led_timeup.on()
        self._score_bord.outputFoul()

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

    def _lightOn(self, light_index:int):
        """ライト点灯処理"""
        self._lightes[light_index].on()
        self._buzzer_l.beep()

    def _lightHit(self, light_index:int):
        """ライト消灯処理"""
        self._lightes[light_index].off()
        self._buzzer_h.beep()

    def _isHit(self, btn_idx:int):
        return self._buttons[btn_idx].isOn()

# ==================
# テストコード
# ================== 
class ReflexesGameTester:
    """テスタークラス"""
    LIGHTS = [Led(2), Led(4), Led(6), Led(8), Led(10), Led(12)]
    BUTTONS = [InputSwitch(3), InputSwitch(5), InputSwitch(7), InputSwitch(9), InputSwitch(11), InputSwitch(13)]
    BUZZER_L = Buzzer(17)
    BUZZER_H = Buzzer(16)
    LED_HIGHSCORE = Led(14)
    LED_TIMEISUP = Led(15)

    def __init__(self):
        self.SCOREBORD = ScoreBord(0, 21, 20)
        self.SCOREBORD.setEngPin(22)
        self.SCOREBORD.setI2cAddr(0x70)
        self._clz = ReflexesGame(self.LIGHTS
                             , self.BUTTONS
                             , self.BUZZER_L
                             , self.BUZZER_H
                             , self.SCOREBORD
                             , self.LED_HIGHSCORE
                             , self.LED_TIMEISUP)

    def orderListTest(self):
        print("len:5 cnt:3")
        print(self._clz.initGame(5, 3))
        print("len:10 cnt:6")
        print(self._clz.initGame(10, 6))

    def endLightTest(self):
        """結果ライト点灯"""
        print("High Score!")
        self._clz._updateScore(2000)
        utime.sleep(5)
        self._clz._initDisplay()
        print("Time Up.")
        self._clz._timeOver(5)
        utime.sleep(5)
        self._clz._initDisplay()
    
    def startGame(self):
        """ゲーム開始"""
        self._clz.gameStert()

if __name__  == "__main__":
    print("test")
    tester = ReflexesGameTester()
    # 点灯順番生成
    tester.orderListTest()
    # 結果ライト点灯
    tester.endLightTest()
    # ゲーム開始
    tester.startGame()