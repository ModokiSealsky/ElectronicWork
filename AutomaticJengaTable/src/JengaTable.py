from machine import PWM, Pin
import utime
from pico.Led import Led
from pico.Servo import Servo
from pico.StepMoter import StepMoter

# GPIO定義
P_READ_SW = 28               # 起動スイッチ
P_STEP_MT = [2, 3, 4, 5] # エレベーター用ステップモーター
P_TURN_SV = 1                # エレベーター用ターンテーブルサーボ
P_PUSH_SV = 0                # 押し出し機用サーボ
P_EXEC_LT = 16               # 動作中LED

# 待ち時間定義
WT_TURN = 1
WT_PUSH = 1

# エレベーター制御クラス
class Elevator:
    def __init__(self, step_pin_no_array, turn_pin_no):
        # ステッピングモーターインスタンス作成
        self.step_mt = StepMoter(
            step_pin_no_array[0],
            step_pin_no_array[1],
            step_pin_no_array[2],
            step_pin_no_array[3]
        )
        # ターンテーブルインスタンス作成
        self.turn_sv = Servo(turn_pin_no)
        # 管理値を初期化
        self.turn_sv.turn(0)
        self.level = 0
        self.step = 1
        self.reload_level = 10
        self.is_turned = False
        
    def reload_start(self):
        """エレベーターをゲーム位置から装填開始位置へ移動
        """
        self.step_mt.step(1200)

    def down(self):
        """エレベーターを1段分下降
        """
        self.step_mt.step(120)
        
    def turn(self):
        """ターンテーブルの向きを変更
        """
        if self.is_turned:
            self.is_turned = False
            self.turn_sv.turn(0)
            print("縦へ")
        else:
            self.is_turned = True
            self.turn_sv.turn(90)
            print("横へ")

    def up(self):
        """エレベーターをゲーム位置まで上昇
        """
        self.step_mt.step(-960)

# 装填クラス
class Pusher:
    def __init__(self, pin_no):
        self.sv = Servo(pin_no)
        self.sv.turn(0)

    def push(self):
        """ジェンガを1個押し出し
        """
        self.sv.turn(180)
        utime.sleep_ms(1000)
        self.sv.turn(0)
        utime.sleep_ms(1000)

# ジェンガ組み立て処理
def relord(elevetor, pusher):
    print("reload start")
    elevetor.reload_start()
    for lv_cnt in range(6):
        print("lv_cnt:" + str(lv_cnt))
        for p_cnt in range(3):
            pusher.push()
        utime.sleep(WT_TURN)
        elevetor.down()
        elevetor.turn()
        utime.sleep(WT_TURN)
    elevetor.up()
    print("reload end")

# メイン処理
switch_counter = 0
switch = Pin(P_READ_SW, Pin.IN, Pin.PULL_DOWN)
elevator = Elevator(P_STEP_MT, P_TURN_SV)
pusher = Pusher(P_PUSH_SV)
light = Led(P_EXEC_LT)
print("start")
while True:
    if switch.value() == 1:
        switch_counter += 1
        #print("on:" + str(switch_counter))
    else:
        switch_counter = 0
        #print("off")
    if switch_counter > 2:
        light.on()
        switch_counter = 0
        relord(elevator, pusher)
        light.off()
    utime.sleep(1)
print("end")