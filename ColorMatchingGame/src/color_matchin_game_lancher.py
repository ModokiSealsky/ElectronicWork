import time
from machine import ADC

from picolib import ColorLed, InputSwitch, PwmBuzzer, TriggerButton
from color_matching_game import (
    ColorMatingGame,
    GameMode,
    ScoreBord,
    TimeBord,
)

# ボリューム取得 ======================================
red_volume = ADC(0)
green_volume = ADC(1)
blue_volume = ADC(2)
# LED初期化 ========================================
master_led = ColorLed(2)
player_led = ColorLed(3)
support_led = ColorLed(4)
master_led.off()
player_led.off()
support_led.off()
# サウンドブザー取得 =====================================
buzzer = PwmBuzzer(0)
# 入力ボタン取得 =======================================
button = TriggerButton(22, True)
# ディスプレイ取得 ======================================
scorebord = ScoreBord()
timebord = TimeBord()
# ゲームクラス生成 ======================================
game = ColorMatingGame()
game.setInputVaolumes(red_volume, green_volume, blue_volume)
game.setColorLeds(master_led, player_led, support_led)
game.setBuzzer(buzzer)
game.set_button(button)
game.set_scorebord(scorebord)
game.set_timebord(timebord)
# ゲーム難易スイッチ取得 ====================================
mode_sw_eazy = InputSwitch(18, True)
mode_sw_normal = InputSwitch(19, True)
mode_sw_hard = InputSwitch(20, True)
mode_sw_expart = InputSwitch(21, True)


# ゲーム難易度取得処理 ====================================
def getGameLevel() -> int:
    if mode_sw_eazy.is_on():
        return GameMode.EASY
    if mode_sw_normal.is_on():
        return GameMode.NORMAL
    if mode_sw_hard.is_on():
        return GameMode.HARD
    return GameMode.EXPERT


# ゲーム開始待機ループ ====================================
def main_roop():
    while True:
        button.refresh()
        if button.is_on_trriger:
            game.set_game_level(getGameLevel())
            game.game_start()
        time.sleep_ms(100)


# エンドポイント =======================================
if __name__ != "__main__":
    main_roop()
else:
    # ==================
    # テストコード
    # ==================
    print("test start ----")
    print("test end   ----")
