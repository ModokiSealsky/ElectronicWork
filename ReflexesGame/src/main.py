"""反応速度を測るゲーム_メイン(待機)ループ"""
from machine import Pin
import utime
from .__init__ import Buzzer ,ReflexesGame ,ScoreBord

# ピン指定 ------------------------------------------------
P_BUZZER_L  = 0
P_BUZZER_H  = 0
P_LIGHTS    = [0,1,2,3,4,5,6,7]
P_BUTTONS   = [0,1,2,3,4,5,6,7]
P_START_BTN = 0
P_HIGHSCORE = 0
P_GAMEOVER  = 0
CH_7SEG_DP  = 0
P_7SEG_SDA  = 1
P_7SEG_SCL  = 2
# ---------------------------------------------------------

# セットアップ ---------------------------------------------
highe_score = 9999
buzzer_l = Buzzer(P_BUZZER_L)
buzzer_h = Buzzer(P_BUZZER_H)
start_btn = Pin(P_START_BTN, Pin.IN)
light_highscore = Pin(P_HIGHSCORE, Pin.OUT)
light_gameover = Pin(P_GAMEOVER, Pin.OUT)
score_bord = ScoreBord(CH_7SEG_DP, P_7SEG_SCL, P_7SEG_SDA)
game_logic = ReflexesGame(P_LIGHTS, P_BUTTONS
                          , buzzer_l, buzzer_h
                          , score_bord)
# ---------------------------------------------------------

# 待機ループ -----------------------------------------------
start_btn_cnt = 0
while True:
    if start_btn.value() == 1:
        start_btn_cnt += 1
    else:
        start_btn_cnt = 0
    if start_btn_cnt > 2:
        print("ゲームスタート")
        light_highscore.off()
        light_gameover.off()
        game_logic.gameStert()
        if game_logic.isScoreUpdated():
            light_highscore.on()
    utime.sleep_ms(1000)
# ---------------------------------------------------------
