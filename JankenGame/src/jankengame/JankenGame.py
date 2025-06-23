import random, utime

from micropython import const
from machine import Pin

from picolib import InputSwitch, Led
from .JankenInfo import JankenInfo
from .JankenScreen import JankenScreen
from .JankenVoice import JankenVoice

class JankenGameMode:
    """じゃんけんゲーム難易度"""
    NORMAL: int = const(0)
    """通常"""
    ENTERTAINMENT: int = const(1)
    """接待(必ず5勝できる)"""
    KICHIKU = const(2)
    """鬼畜(必ず負ける)"""
    FIRST_GU: int = const(3)
    """最初はグー(ランダム要素あり)"""

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

    def __init__(self,
                 janken_screen: JankenScreen,
                 led_ply_gu: Led, led_ply_ch: Led, led_ply_pa: Led,
                 btn_gu: InputSwitch,
                 btn_ch: InputSwitch,
                 btn_pa: InputSwitch,
                 voice: JankenVoice,
                 info: JankenInfo):
        self._screen = janken_screen
        self._led_ply_gu = led_ply_gu
        self._led_ply_ch = led_ply_ch
        self._led_ply_pa = led_ply_pa
        self._ply_gu_btn = btn_gu
        self._ply_ch_btn = btn_ch
        self._ply_pa_btn = btn_pa
        self._voice = voice
        self._info = info

    def _get_player_hand(self, wait_ms: int = 1000) -> int:
        """プレイヤーの手を取得する"""
        clock = 0
        while clock < wait_ms:
            if self._ply_gu_btn.is_on():
                return JankenGame.Hand.PLY_GU
            if self._ply_ch_btn.is_on():
                return JankenGame.Hand.PLY_CH
            if self._ply_pa_btn.is_on():
                return JankenGame.Hand.PLY_PA
            utime.sleep_ms(1)
        return JankenGame.Hand.PLY_NO

    def _get_Cpu_hand(self):
        """コンピューターの手をランダムで決定する"""
        return random.randint(0, 2)

    def _get_cpu_win_hand(self, player_value: int) -> int:
        """コンピューターが勝つ手を取得する"""
        if player_value == JankenGame.Hand.PLY_GU:
            return JankenGame.Hand.CPU_PA
        elif player_value == JankenGame.Hand.PLY_CH:
            return JankenGame.Hand.CPU_GU
        else:
            return JankenGame.Hand.CPU_CH

    def _get_cpu_lose_hand(self, player_value: int) -> int:
        """コンピューターが負ける手を取得する"""
        if player_value == JankenGame.Hand.PLY_GU:
            return JankenGame.Hand.CPU_CH
        elif player_value == JankenGame.Hand.PLY_CH:
            return JankenGame.Hand.CPU_PA
        else:
            return JankenGame.Hand.CPU_GU

    def _check_player_win(self, player_value: int, cpu_value: int) -> int:
        """プレイヤー勝利判定

        * 0:あいこ
        * 1:負け
        * 2:勝ち
        """
        return (player_value - cpu_value) % 3

    def _show_cpu_hand(self, cpu_value:int) -> None:
        """CPUの手を表示する"""
        if cpu_value == JankenGame.Hand.CPU_GU:
            self._screen.show_gu()
        elif cpu_value == JankenGame.Hand.CPU_CH:
            self._screen.show_ch()
        else:
            self._screen.show_pa()

    def _hidden_cpu_hand(self) -> None:
        """CPUの手を非表示にする"""
        self._screen.hand_off()

    def _game_normal(self, victory_count = 0) -> int:
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

    def _game_entertainment(self) -> int:
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

    def _game_kichiku(self) -> int:
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

    def game_start(self, janken_game_mode: int) -> None:
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
    # スクリーンの手用LED
    led_gu = Led(2)
    led_ch = Led(3)
    led_pa = Led(4)
    led_g_c = Led(5)
    led_c_p = Led(6)
    # 結果表示用LED
    led_w = Led(7)
    led_d = Led(8)
    led_l = Led(9)
    # スクリーン初期化
    screen = JankenScreen([led_gu, led_g_c],
                       [led_ch, led_g_c, led_c_p],
                       [led_pa, led_c_p],
                       led_w, led_d, led_l)
    # プレイヤーの手用LED
    led_p_gu = Led(10)
    led_p_ch = Led(11)
    led_p_pa = Led(12)
    btn_gu = InputSwitch(18)
    btn_ch = InputSwitch(19)
    btn_pa = InputSwitch(20)

    voice = JankenVoice()
    info = JankenInfo()
    clz = JankenGame(screen, led_p_gu, led_p_ch, led_p_pa,
                     btn_gu, btn_ch, btn_pa,
                     voice, info)
    print("test end   -----")
