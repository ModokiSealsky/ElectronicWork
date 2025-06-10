"""反応速度を測るゲーム_メイン(待機)ループ"""
import utime
from .__init__ import Buzzer, InputSwitch, Led ,ReflexesGame ,ScoreBord

# ピン指定 ---------------------------------------------------------------------
P_BUZZER_L  = 17
P_BUZZER_H  = 16
P_LIGHTS    = [2 ,4 ,6, 8, 10, 12]
P_BUTTONS   = [3, 5, 7, 9, 11, 13]
P_START_BTN = 19
P_HIGHSCORE = 14
P_GAMEOVER  = 15
CH_7SEG_DP  = 0
ADD_7SEG_D  = 0x70
P_7SEG_SDA  = 20
P_7SEG_SCL  = 21
P_7SEG_ENG  = 22
# ------------------------------------------------------------------------------

# セットアップ -----------------------------------------------------------------
start_btn = InputSwitch(P_START_BTN)
score_bord = ScoreBord(CH_7SEG_DP, P_7SEG_SCL, P_7SEG_SDA)
score_bord.setEngPin(P_7SEG_ENG)
score_bord.setI2cAddr(ADD_7SEG_D)
game_logic = ReflexesGame([Led(pin_no) for pin_no in P_LIGHTS]
                          , [InputSwitch(pin_no) for pin_no in P_BUTTONS]
                          , Buzzer(P_BUZZER_L)
                          , Buzzer(P_BUZZER_H)
                          , score_bord
                          , Led(P_HIGHSCORE)
                          , Led(P_GAMEOVER))
# ------------------------------------------------------------------------------

# 待機ループ -------------------------------------------------------------------
start_btn_cnt = 0
while True:
    if start_btn.isOn():
        start_btn_cnt += 1
    else:
        start_btn_cnt = 0
    if start_btn_cnt > 2:
        print("ゲームスタート")
        game_logic.gameStert()
    utime.sleep_ms(1000)
# ------------------------------------------------------------------------------
