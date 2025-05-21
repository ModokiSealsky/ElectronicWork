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

    def _getPlayerHand(self, wait_ms:int = 1000):
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

    def _getCpuHand(self):
        """コンピューターの手をランダムで決定する"""
        return random.randint(0, 2)

    def _getCpuWinHand(self, player_value:int):
        """コンピューターが勝つ手を取得する"""
        if player_value == self._PLY_GU:
            return self._CPU_PA
        elif player_value == self._PLY_CH:
            return self._CPU_GU
        else:
            return self._CPU_CH

    def _getCpuLoseHand(self, player_value:int):
        """コンピューターが負ける手を取得する"""
        if player_value == self._PLY_GU:
            return self._CPU_PA
        elif player_value == self._PLY_CH:
            return self._CPU_PA
        else:
            return self._CPU_GU

    def _checkPlayerVWin(self, player_value:int, cpu_value:int):
        """プレイヤー勝利判定

        * 0:あいこ
        * 1:負け
        * 2:勝ち
        """
        return (player_value - cpu_value) % 3

    def _showCpuHand(self, cpu_value:int):
        """CPUの手を表示する"""
        self._cpu_leds[cpu_value].on()

    def _hiddenCpuHand(self):
        """CPUの手を非表示にする"""
        self._cpu_leds[self._CPU_GU].off()
        self._cpu_leds[self._CPU_CH].off()
        self._cpu_leds[self._CPU_PA].off()

    def _gameNormal(self, victory_count = 0):
        """ゲーム(通常モード)"""
        cpu_val = self._NONE
        ply_val = self._NONE
        while(victory_count < 9):
            cpu_val = self._getCpuHand()
            self._voice.callJan()
            ply_val = self._getPlayerHand()
            if ply_val == self._NONE:
                self._voice.callKen()
                ply_val = self._getPlayerHand()
            if ply_val == self._NONE:
                ply_val = self._getPlayerHand(200)
            if ply_val == self._NONE:
                self._voice.callTimeUp()
                return victory_count
            self._voice.callPon()
            self._showCpuHand(cpu_val)
            chk_val = self._checkPlayerVWin(ply_val, cpu_val)
            if chk_val == self._LOSE:
                self._voice.callLose()
                return victory_count
            elif chk_val == self._DROW:
                self._voice.callDraw()
            else:
                self._voice.callWin()
                victory_count += 1
        # 9勝達成
        self._voice.callVictory()
        return victory_count

    def _gameEntertainment(self):
        """ゲーム(接待モード)"""
        victory_count = 0
        while(victory_count < 5):
            self._voice.callJan()
            ply_val = self._getPlayerHand()
            if ply_val == self._NONE:
                self._voice.callKen()
                ply_val = self._getPlayerHand()
            if ply_val == self._NONE:
                ply_val = self._getPlayerHand(200)
            if ply_val == self._NONE:
                self._voice.callTimeUp()
                return victory_count
            self._voice.callPon()
            self._showCpuHand(self._getCpuLoseHand(ply_val))
            self._voice.callWin()
            victory_count += 1
        return self._gameNormal(victory_count)

    def _gameKichiku(self):
        """ゲーム(鬼畜モード)"""
        self._voice.callJan()
        ply_val = self._getPlayerHand()
        if ply_val == self._NONE:
            self._voice.callKen()
            ply_val = self._getPlayerHand()
        if ply_val == self._NONE:
            ply_val = self._getPlayerHand(200)
        if ply_val == self._NONE:
            self._voice.callTimeUp()
            return 0
        self._voice.callPon()
        self._showCpuHand(self._getCpuWinHand(ply_val))
        self._voice.callLose()
        return 0

    def gameStart(self, mode:int):
        """ゲーム開始"""
        if mode == self.MODE_ENTERTAINMENT:
            self._gameEntertainment()
        elif mode == self.MODE_KICHIKU:
            self._gameKichiku()
        else:
            self._gameNormal()

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start -----")
    voice = JankenVoice()
    clz = JankenGame(0, 1, 2, 3, 4, 5, voice)
    print("test end   -----")
