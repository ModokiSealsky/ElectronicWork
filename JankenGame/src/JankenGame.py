from machine import Pin
from .JankenVoice import JankenVoice
import random, utime

class JankenGame:
    """じゃんけんゲームクラス
    
    ジャンケンの手を下記の値で定義する
    * 0: CPUのグー
    * 1: CPUのチョキ
    * 2: CPUのパー
    * 3: プレイヤーのグー
    * 4: プレイヤーのチョキ
    * 5: プレイヤーのパー

    勝敗を下記の値で定義する
    * 0: あいこ
    * 1: 負け
    * 2: 勝ち
    """
    _CPU_GU = 0
    _CPU_CH = 1
    _CPU_PA = 2
    _PLY_GU = 3
    _PLY_CH = 4
    _PLY_PA = 5

    _NONE = -1

    _DROW = 0
    _LOSE = 1
    _WIN =2

    MODE_ENTERTAINMENT = 1
    """モード:接待"""
    MODE_KICHIKU = 2
    """モード:鬼畜"""

    _victory_count = 0
    """連勝数"""

    _high_score = 0
    """最高得点"""

    def __init__(self, ply_gu_pin:int, ply_ch_pin:int, ply_pa_pin:int, led_gu_pin:int, led_ch_pin:int, led_pa_pin:int, voice:JankenVoice):
        self._ply_gu_btn = Pin(ply_gu_pin, Pin.IN)
        self._ply_ch_btn = Pin(ply_ch_pin, Pin.IN)
        self._ply_pa_btn = Pin(ply_pa_pin, Pin.IN)
        self._cpu_leds = [
            Pin(led_gu_pin, Pin.OUT, Pin.PULL_UP),
            Pin(led_ch_pin, Pin.OUT, Pin.PULL_UP),
            Pin(led_pa_pin, Pin.OUT, Pin.PULL_UP)
        ]
        self._voice = voice

    def _get_player_hand(self, wait_ms:int = 1000):
        """プレイヤーの手を取得する"""
        clock = 0
        while clock < wait_ms:
            if self._ply_gu_btn.value == 1:
                return self._PLY_GU
            if self._ply_ch_btn.value == 1:
                return self._PLY_CH
            if self._ply_pa_btn.value == 1:
                return self._PLY_PA
            utime.sleep_ms(1)
        return self._NONE

    def _get_Cpu_hand(self):
        """コンピューターの手をランダムで決定する"""
        return random.randint(0, 2)

    def _get_cpu_win_hand(self, player_value:int):
        """コンピューターが勝つ手を取得する"""
        if player_value == self._PLY_GU:
            return self._CPU_PA
        elif player_value == self._PLY_CH:
            return self._CPU_GU
        else:
            return self._CPU_CH

    def _get_cpu_lose_hand(self, player_value:int):
        """コンピューターが負ける手を取得する"""
        if player_value == self._PLY_GU:
            return self._CPU_PA
        elif player_value == self._PLY_CH:
            return self._CPU_PA
        else:
            return self._CPU_GU

    def _check_player_win(self, player_value:int, cpu_value:int):
        """プレイヤー勝利判定

        * 0:あいこ
        * 1:負け
        * 2:勝ち
        """
        return (player_value - cpu_value) % 3

    def _show_cpu_hand(self, cpu_value:int):
        """CPUの手を表示する"""
        self._cpu_leds[cpu_value].on()

    def _hidden_cpu_hand(self):
        """CPUの手を非表示にする"""
        self._cpu_leds[self._CPU_GU].off()
        self._cpu_leds[self._CPU_CH].off()
        self._cpu_leds[self._CPU_PA].off()

    def _game_normal(self, victory_count = 0):
        """ゲーム(通常モード)"""
        cpu_val = self._NONE
        ply_val = self._NONE
        while(victory_count < 9):
            cpu_val = self._get_Cpu_hand()
            self._voice.call_jan()
            ply_val = self._get_player_hand()
            if ply_val == self._NONE:
                self._voice.call_ken()
                ply_val = self._get_player_hand()
            if ply_val == self._NONE:
                ply_val = self._get_player_hand(200)
            if ply_val == self._NONE:
                self._voice.call_timeUp()
                return victory_count
            self._voice.call_pon()
            self._show_cpu_hand(cpu_val)
            chk_val = self._check_player_win(ply_val, cpu_val)
            if chk_val == self._LOSE:
                self._voice.call_lose()
                return victory_count
            elif chk_val == self._DROW:
                self._voice.call_draw()
            else:
                self._voice.call_win()
                victory_count += 1
        # 9勝達成
        self._voice.call_victory()
        return victory_count

    def _game_entertainment(self):
        """ゲーム(接待モード)"""
        victory_count = 0
        while(victory_count < 5):
            self._voice.call_jan()
            ply_val = self._get_player_hand()
            if ply_val == self._NONE:
                self._voice.call_ken()
                ply_val = self._get_player_hand()
            if ply_val == self._NONE:
                ply_val = self._get_player_hand(200)
            if ply_val == self._NONE:
                self._voice.call_timeUp()
                return victory_count
            self._voice.call_pon()
            self._show_cpu_hand(self._get_cpu_lose_hand(ply_val))
            self._voice.call_win()
            victory_count += 1
        return self._game_normal(victory_count)

    def _game_kichiku(self):
        """ゲーム(鬼畜モード)"""
        self._voice.call_jan()
        ply_val = self._get_player_hand()
        if ply_val == self._NONE:
            self._voice.call_ken()
            ply_val = self._get_player_hand()
        if ply_val == self._NONE:
            ply_val = self._get_player_hand(200)
        if ply_val == self._NONE:
            self._voice.call_timeUp()
            return 0
        self._voice.call_pon()
        self._show_cpu_hand(self._get_cpu_win_hand(ply_val))
        self._voice.call_lose()
        return 0

    def game_start(self, mode:int):
        """ゲーム開始"""
        if mode == self.MODE_ENTERTAINMENT:
            self._game_entertainment()
        elif mode == self.MODE_KICHIKU:
            self._game_kichiku()
        else:
            self._game_normal()

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start -----")
    voice = JankenVoice()
    clz = JankenGame(0, 1, 2, 3, 4, 5, voice)
    print("test end   -----")
