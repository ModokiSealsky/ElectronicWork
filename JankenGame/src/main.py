import utime

from micropython import const

from picolib import Buzzer, InputSwitch, Led
from jankengame import JankenGame, JankenGameMode,JankenInfo, JankenScreen, JankenVoice

# ピン指定 ---------------------------------------------------------------------
P_LED_CPU_GU = const(2)
P_LED_CPU_CH = const(3)
P_LED_CPU_PA = const(4)
P_LED_CPU_AL = const(5)
P_LED_CPU_GC = const(6)
P_LED_CPU_CP = const(7)
P_LED_WIN = const(8)
P_LED_DROW = const(9)
P_LED_LOSE = const(10)
# ------------------------------
P_LED_PLY_GU = const(11)
P_LED_PLY_CH = const(12)
P_LED_PLY_PA = const(13)
# ------------------------------
P_BTN_GU = const(18)
P_BTN_CH = const(19)
P_BTN_PA = const(20)
# ------------------------------
P_BTN_ST = const(21)
P_MODE_A = const(16)
P_MODE_B = const(17)
# ------------------------------
P_BUZZER_L = const(26)
P_BUZZER_H = const(27)
# ------------------------------
P_I2C_0_SDA = const(0)
P_I2C_0_SCL = const(1)
P_I2C_1_SDA = const(14)
P_I2C_1_SCL = const(15)
ADDR_INFO = const(0x70)
ADDR_VOICE = const(0x00)
# ------------------------------------------------------------------------------

# セットアップ -----------------------------------------------------------------
# スクリーン
led_gu = Led(P_LED_CPU_GU)
led_ch = Led(P_LED_CPU_CH)
led_pa = Led(P_LED_PLY_PA)
led_al = Led(P_LED_CPU_AL)
led_gc = Led(P_LED_CPU_GC)
led_cp = Led(P_LED_CPU_CP)
screen = JankenScreen(
    [led_gu, led_al, led_gc],
    [led_ch, led_al, led_cp],
    [led_pa, led_al, led_cp],
    Led(P_LED_WIN),
    Led(P_LED_DROW),
    Led(P_LED_LOSE)
)
# 掛け声
voice = JankenVoice()

# 情報表示
info = JankenInfo()

# プレイヤー入力
led_ply_gu = Led(P_LED_PLY_GU)
led_ply_ch = Led(P_LED_PLY_CH)
led_ply_pa = Led(P_LED_PLY_PA)
btn_gu = InputSwitch(P_BTN_GU)
btn_ch = InputSwitch(P_BTN_CH)
btn_pa = InputSwitch(P_BTN_PA)

# ゲーム
game_logic = JankenGame(
    screen, led_ply_gu,
    led_ply_ch,
    led_ply_pa,
    btn_gu,
    btn_ch,
    btn_pa,
    voice,
    info
)

# ------------------------------------------------------------------------------
mode_a = InputSwitch(P_MODE_A)
mode_b = InputSwitch(P_MODE_B)
btn_start = InputSwitch(P_BTN_ST)
def get_game_mode() -> int:
    """ゲームモード取得"""
    if mode_a.is_on() and mode_b.is_on():
        return JankenGameMode.ENTERTAINMENT
    if mode_a.is_on():
        return JankenGameMode.KICHIKU
    if mode_b.is_on():
        return JankenGameMode.FIRST_GU
    return JankenGameMode.NORMAL

# ゲーム開始待ちループ -----------------------------------------------------------
start_btn_cnt: int = 0
while True:
    if btn_start.is_on():
        start_ctn_cnt += 1
    else:
        start_btn_cnt = 0
    if start_btn_cnt > 1:
        game_logic.game_start(get_game_mode())
        start_btn_cnt = 0
# ------------------------------------------------------------------------------
