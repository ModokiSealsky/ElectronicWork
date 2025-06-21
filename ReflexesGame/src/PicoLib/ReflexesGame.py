import utime
import random
import _thread

from PicoLib import Buzzer, InputSwitch, Led, ScoreBord

class ReflexesGame:
    """反応速度を測るゲーム処理クラス"""

    _high_score = 1
    """ 最高得点 """

    _last_score = 1
    """ 前回得点 """

    _is_waiting_mode = True
    """ゲーム開始待ち状態フラグ"""

    def __init__(self
                 , lightes: list[Led]
                 , buttons: list[InputSwitch]
                 , buzzer_l: Buzzer
                 , buzzer_h: Buzzer
                 , score_bord: ScoreBord
                 , led_highscore: Led
                 , led_timeup: Led
                 , order_size: int = 10):
        """初期化

            Aggs:
                lights: ライト用LED配列
                buttons: ボタン配列
                buzzer_l: 低音ブザー
                buzzer_h: 高音ブザー
                score_bord: 点数表示用ディスプレイ
                led_highscore: スコア更新LED
                led_timeup: 時間切れLED
                order_size: ゲーム終了までのボタン順の長さ(デフォルト10)
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

    def parts_check(self):
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
        self._score_bord.display_check()
        # ボタンチェック 2個以上同時押しで終了
        btn_cnt = 0
        while btn_cnt < 2:
            btn_cnt = 0
            for b in self._buttons:
                if b.is_on():
                    self._buzzer_l.beep()
                    btn_cnt += 1
        self._init_display()

    def _init_display(self):
        """表示系初期化"""
        self._led_highscore.off()
        self._led_timeup.off()
        for light_idx in range(self._BUTTON_COUNT):
            self._lightes[light_idx].off()

    def order_shafle(self, order_list_size:int, button_count:int):
        """ゲーム初期化
        
            ゲーム中のボタン順をランダムで生成する。
            (同一ボタンが連続で設定されないように調整済)

        Args:
            order_list_size: ボタン順番の長さ(クリアまでのボタン数)
            button_count: ゲームボタン数
        """
        order_list:list[int] = []
        for order_idx in range(order_list_size):
            target_idx = random.randint(1, button_count) % button_count
            if order_idx > 0 and order_list[order_idx - 1] == target_idx:
                target_idx = (target_idx + 1) % button_count
            order_list.append(target_idx)
        return order_list

    def game_stert(self):
        """ゲーム開始"""
        print("Game Start!")
        # 待機時アニメーション停止
        self._is_waiting_mode = False
        self._buzzer_h.beep(1000)
        utime.sleep_ms(500)
        # 初期化
        self._init_display()
        order_list = self.order_shafle(self._ORDER_LIST_SIZE, self._BUTTON_COUNT)
        # 開始処理
        self._start_signal()
        self._score_bord.counter_start(9999)
        # ゲーム開始
        self._game_roop(order_list)
        # 待機アニメーション開始
        self._waiting_thread_start()

    def _game_roop(self, order_list: list[int]):
        """ゲーム処理ループ
        
            Args:
                order_list: ボタン順リスト 
        """
        score = 9999
        order_idx = 0
        now_target = order_list[order_idx]
        self._light_on(now_target)
        while score >= 0:
            self._score_bord.counter_update(score)
            # 正解判定
            if self._isHit(now_target):
                self._light_hit(now_target)
                order_idx += 1
                # ゲーム終了判定
                if order_idx >= self._ORDER_LIST_SIZE:
                    self._game_finish(score)
                    self._waiting_thread_start()
                    print("----")
                    return
                now_target = order_list[order_idx]
                self._light_on(now_target)
            score -= 1
            utime.sleep_us(800)
        # タイムオーバー処理
        self._time_over(order_idx)

    def _game_finish(self, score:int):
        """ゲーム終了"""
        self._last_score = score
        self._buzzer_l.beep(500)
        utime.sleep_ms(100)
        self._buzzer_h.beep(1000)
        self._score_bord.counter_stop(score)
        self._score_bord.output_clear()
        if score > self._high_score:
            self._update_score(score)

    def _update_score(self, score:int):
        """ハイスコア更新

        Args:
            score: ゲームスコア
        """
        self._high_score = score
        self._led_highscore.on()
        utime.sleep(1)
        self._buzzer_l.beep(50)
        utime.sleep_ms(50)
        self._buzzer_l.beep(50)
        utime.sleep_ms(50)
        self._buzzer_h.beep(1000)

    def _time_over(self, order_idx:int):
        """時間切れゲームオーバー処理

        Args:
            order_idx: 現在の表示順(何個目まで進んだかを把握)
        """
        print("Time Over! {0:02}".format(self._ORDER_LIST_SIZE - order_idx))
        self._last_score = 0
        self._score_bord.counter_stop(0)
        self._buzzer_l.beep(1000)
        self._led_timeup.on()
        self._score_bord.output_foul()

    def _start_signal(self):
        """ゲーム開始時演出"""
        self._score_bord.output_message("# 3#")
        self._buzzer_l.beep()
        utime.sleep_ms(800)
        self._score_bord.output_message("= 2=")
        self._buzzer_l.beep()
        utime.sleep_ms(800)
        self._score_bord.output_message("_ 1_")
        self._buzzer_l.beep()
        utime.sleep_ms(800)
        self._score_bord.output_message("GO!!")
        self._buzzer_h.beep(500)

    def _light_on(self, light_index:int):
        """ライト点灯処理"""
        self._buzzer_l.beep()
        self._lightes[light_index].on()

    def _light_hit(self, light_index:int):
        """ライト消灯処理"""
        self._lightes[light_index].off()
        self._buzzer_h.beep()

    def _isHit(self, btn_idx:int):
        return self._buttons[btn_idx].is_on()

    def _waiting_animation(self):
        """ゲーム開始待ち中アニメーション"""
        print("Wait Animation Start.")
        utime.sleep(5)
        is_show_highscore = False
        while self._is_waiting_mode:
            if is_show_highscore:
                if self._last_score < 1:
                    self._score_bord.output_foul()
                    self._led_timeup.on()
                else:
                    self._score_bord.output_count(self._last_score)
                self._led_highscore.off()
                is_show_highscore = False
            else:
                self._score_bord.output_count(self._high_score)
                self._led_highscore.on()
                self._led_timeup.off()
                is_show_highscore = True
            utime.sleep(2)
        self._init_display()
        print("Wait Animation End.")

    def _waiting_thread_start(self):
        if self._is_waiting_mode:
            return
        self._is_waiting_mode = True
        self._waiting_thread = _thread.start_new_thread(self._waiting_animation, ())        

# ==================
# テストコード
# ================== 
class ReflexesGameTester:
    """テスタークラス"""
    LIGHTS = [Led(2), Led(4), Led(6), Led(8), Led(10), Led(12)]
    BUTTONS = [
        InputSwitch(3),
        InputSwitch(5),
        InputSwitch(7),
        InputSwitch(9),
        InputSwitch(11),
        InputSwitch(13)
        ]
    BUZZER_L = Buzzer(17)
    BUZZER_H = Buzzer(16)
    LED_HIGHSCORE = Led(14)
    LED_TIMEISUP = Led(15)

    def __init__(self):
        self.SCOREBORD = ScoreBord(0, 21, 20)
        # self.SCOREBORD.setEngPin(22)
        self.SCOREBORD.set_i2c_addr(0x70)
        self._clz = ReflexesGame(self.LIGHTS, self.BUTTONS,
                                 self.BUZZER_L, self.BUZZER_H,
                                 self.SCOREBORD, self.LED_HIGHSCORE,
                                 self.LED_TIMEISUP)

    def order_list_test(self):
        print("len:5 cnt:3")
        print(self._clz.order_shafle(5, 3))
        print("len:10 cnt:6")
        print(self._clz.order_shafle(10, 6))

    def parts_check(self):
        """各パーツチェック"""
        print("Parts Check Start")
        self._clz.parts_check()
        print("Parts Check End")
    
    def start_game(self):
        """ゲーム開始"""
        self._clz.game_stert()

if __name__  == "__main__":
    print("test")
    tester = ReflexesGameTester()
    # 点灯順番生成
    tester.order_list_test()
    # 各パーツチェック
    tester.parts_check()
    # ゲーム開始
    tester.start_game()