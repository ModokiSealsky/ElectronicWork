"""反応速度を測るゲームv2_メイン(待機)ループ"""

import utime

from PicoLib import PwmBuzzer, InputSwitch, InputAdc, TriggerButton, Led
from reflexesgame import (
    ReflexesGame,
    ResultLight,
    ScoreBordDig4Seg7,
    SoundEffectUnitByPwm,
)

# ピン指定 ---------------------------------------------------------------------
P_LIGHTS = [2, 4, 6, 8, 10, 12, 14, 16, 18]
P_BUTTONS = [3, 5, 7, 9, 11, 13, 15, 17, 19]
P_PWM_BUZZER = 20
P_HIGHSCORE = 21
P_GAMEOVER = 22
P_USE_PENALTY = 26
P_USE_TRRIGER = 27
P_MODE_SEL = 28
CH_7SEG_DP = 0
ADD_7SEG_D = 0x70
P_7SEG_SDA = 0
P_7SEG_SCL = 1
# ------------------------------------------------------------------------------

# セットアップ -----------------------------------------------------------------
# 難易度取得
use_penalty = InputSwitch(P_MODE_SEL).is_on()
print("use_penalty:{0}".format(use_penalty))
use_trriger = InputSwitch(P_MODE_SEL).is_on()
print("use_trriger:{0}".format(use_trriger))
mode_selector_val = InputAdc(P_MODE_SEL).get_parcents_value()
order_size: int
if mode_selector_val > 60:
    print("--Mode:Oni--")
    order_size = 30
elif mode_selector_val > 50:
    print("--Mode:Hard--")
    order_size = 20
elif mode_selector_val > 40:
    print("--Mode:Normal--")
    order_size = 10
else:
    print("--Mode:Eazy--")
    order_size = 5
# ゲーム初期化
lights = [Led(pin_no) for pin_no in P_LIGHTS]
buttons = [TriggerButton(pin_no) for pin_no in P_BUTTONS]
start_btn = buttons[0]
score_bord = ScoreBordDig4Seg7(CH_7SEG_DP, P_7SEG_SCL, P_7SEG_SDA)
score_bord.set_i2c_addr(ADD_7SEG_D)
score_bord.display_check()
se_unit = SoundEffectUnitByPwm(PwmBuzzer(P_PWM_BUZZER))
se_unit.check()
result_lite = ResultLight(Led(P_HIGHSCORE), Led(P_GAMEOVER))
result_lite.check()
game_logic = ReflexesGame(
    lights,
    buttons,
    se_unit,
    score_bord,
    result_lite,
    order_size,
)
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
    utime.sleep_ms(500)
# ------------------------------------------------------------------------------
