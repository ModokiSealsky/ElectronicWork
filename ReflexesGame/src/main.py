"""反応速度を測るゲーム_メイン(待機)ループ"""
import utime

from PicoLib import Buzzer, InputSwitch, Led, ReflexesGame, ScoreBord, ScoreBordDig4Seg7

# ピン指定 ---------------------------------------------------------------------
P_BUZZER_L  = 17
P_BUZZER_H  = 16
P_LIGHTS    = [2 ,4 ,6, 8, 10, 12]
P_BUTTONS   = [3, 5, 7, 9, 11, 13]
P_MODE_SEL  = 18
P_START_BTN = 19
P_HIGHSCORE = 14
P_GAMEOVER  = 15
CH_7SEG_DP  = 0
ADD_7SEG_D  = 0x70
P_7SEG_SDA  = 20
P_7SEG_SCL  = 21
# ------------------------------------------------------------------------------

# セットアップ -----------------------------------------------------------------
# 難易度取得
mode_selector = InputSwitch(P_MODE_SEL)
order_size: int
if mode_selector.is_off():
    print("--Mode:Normal--")
    order_size = 10
else:
    order_size = 20
    print("--Mode:Hard--")
# ゲーム初期化
lights = [Led(pin_no) for pin_no in P_LIGHTS]
start_btn = InputSwitch(P_START_BTN)
score_bord = ScoreBordDig4Seg7(CH_7SEG_DP, P_7SEG_SCL, P_7SEG_SDA)
score_bord.set_i2c_addr(ADD_7SEG_D)
game_logic = ReflexesGame(lights, [InputSwitch(pin_no) for pin_no in P_BUTTONS],
                          Buzzer(P_BUZZER_L), Buzzer(P_BUZZER_H), score_bord,
                          Led(P_HIGHSCORE), Led(P_GAMEOVER),
                          order_size)
game_logic.parts_check()
# ------------------------------------------------------------------------------

# 待機時アニメーション -------------------------------------------------------------------
lights_idx: int = 0
lights_len: int = len(lights)
def waitAnimation(idx: int, _len: int):
    for light in lights:
        light.off()
    idx = (idx + 1) % _len
    lights[idx].on()
    return idx
# ------------------------------------------------------------------------------

# 待機ループ -------------------------------------------------------------------
start_btn_cnt = 0
while True:
    lights_idx = waitAnimation(lights_idx, lights_len)
    if start_btn.is_on():
        start_btn_cnt += 1
    else:
        start_btn_cnt = 0
    if start_btn_cnt > 1:
        print("ゲームスタート")
        game_logic.game_stert()
    utime.sleep_ms(1000)
# ------------------------------------------------------------------------------
