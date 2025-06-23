from machine import Pin
from .JankenVoice import JankenVoice
import random, utime

from micropython import const

class JankenGameMode:
    """じゃんけんゲーム難易度"""
    NORMAL: int = const(0)
    """通常"""
    ENTERTAINMENT: int = const(1)
    """接待(必ず5勝できる)"""
    KICHIKU = const(2)
    """鬼畜(必ず負ける)"""

class JankenGame:
    """じゃんけんゲームクラス
    
    """

    class Hand:
        """じゃんけんの手"""
        CPU_GU: int = const(0)
        """CPUのグー"""
        CPU_CH: int = const(1)
        """CPUのチョキ"""
        CPU_PA: int = const(2)
        """CPUのパー"""
        PLY_GU: int = const(3)
        """プレイヤーのグー"""
        PLY_CH: int = const(4)
        """プレイヤーのチョキ"""
        PLY_PA: int = const(5)
        """プレイヤーのパー"""
        PLY_NO: int = const(-1)
        """プレイヤー未入力"""

    class Result:
        """プレイヤーの勝敗結果"""
        DROW: int = const(0)
        """あいこ"""
        LOSE: int = const(1)
        """負け"""
        WIN: int = const(2)
        """勝ち"""

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
                return JankenGame.Hand.PLY_GU
            if self._ply_ch_btn.value == 1:
                return JankenGame.Hand.PLY_CH
            if self._ply_pa_btn.value == 1:
                return JankenGame.Hand.PLY_PA
            utime.sleep_ms(1)
        return JankenGame.Hand.PLY_NO

    def _get_Cpu_hand(self):
        """コンピューターの手をランダムで決定する"""
        return random.randint(0, 2)

    def _get_cpu_win_hand(self, player_value:int):
        """コンピューターが勝つ手を取得する"""
        if player_value == JankenGame.Hand.PLY_GU:
            return JankenGame.Hand.CPU_PA
        elif player_value == JankenGame.Hand.PLY_CH:
            return JankenGame.Hand.CPU_GU
        else:
            return JankenGame.Hand.CPU_CH

    def _get_cpu_lose_hand(self, player_value:int):
        """コンピューターが負ける手を取得する"""
        if player_value == JankenGame.Hand.PLY_GU:
            return JankenGame.Hand.CPU_CH
        elif player_value == JankenGame.Hand.PLY_CH:
            return JankenGame.Hand.CPU_PA
        else:
            return JankenGame.Hand.CPU_GU

    def _check_player_win(self, player_value:int, cpu_value:int) -> int:
        """プレイヤー勝利判定

        * 0:あいこ
        * 1:負け
        * 2:勝ち
        """
        return (player_value - cpu_value) % 3

    def _show_cpu_hand(self, cpu_value:int) -> None:
        """CPUの手を表示する"""
        self._cpu_leds[cpu_value].on()

    def _hidden_cpu_hand(self) -> None:
        """CPUの手を非表示にする"""
        self._cpu_leds[JankenGame.Hand.CPU_GU].off()
        self._cpu_leds[JankenGame.Hand.CPU_CH].off()
        self._cpu_leds[JankenGame.Hand.CPU_PA].off()

    def _game_normal(self, victory_count = 0):
        """ゲーム(通常モード)"""
        cpu_val = JankenGame.Hand.PLY_NO
        ply_val = JankenGame.Hand.PLY_NO
        while(victory_count < 9):
            cpu_val = self._get_Cpu_hand()
            self._voice.call_jan()
            ply_val = self._get_player_hand()
            if ply_val == JankenGame.Hand.PLY_NO:
                self._voice.call_ken()
                ply_val = self._get_player_hand()
            if ply_val == JankenGame.Hand.PLY_NO:
                ply_val = self._get_player_hand(200)
            if ply_val == JankenGame.Hand.PLY_NO:
                self._voice.call_timeUp()
                return victory_count
            self._voice.call_pon()
            self._show_cpu_hand(cpu_val)
            chk_val = self._check_player_win(ply_val, cpu_val)
            if chk_val == JankenGame.Result.LOSE:
                self._voice.call_lose()
                return victory_count
            elif chk_val == JankenGame.Result.DROW:
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
            if ply_val == JankenGame.Hand.PLY_NO:
                self._voice.call_ken()
                ply_val = self._get_player_hand()
            if ply_val == JankenGame.Hand.PLY_NO:
                ply_val = self._get_player_hand(200)
            if ply_val == JankenGame.Hand.PLY_NO:
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
        if ply_val == JankenGame.Hand.PLY_NO:
            self._voice.call_ken()
            ply_val = self._get_player_hand()
        if ply_val == JankenGame.Hand.PLY_NO:
            ply_val = self._get_player_hand(200)
        if ply_val == JankenGame.Hand.PLY_NO:
            self._voice.call_timeUp()
            return 0
        self._voice.call_pon()
        self._show_cpu_hand(self._get_cpu_win_hand(ply_val))
        self._voice.call_lose()
        return 0

    def game_start(self, janken_game_mode: JankenGameMode):
        """ゲーム開始"""
        if janken_game_mode == JankenGameMode.ENTERTAINMENT:
            self._game_entertainment()
        elif janken_game_mode == JankenGameMode.KICHIKU:
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
