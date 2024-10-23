from machine import PWM, Pin
import utime
from pico.Led import Led
from pico.Servo import Servo
from pico.StepMoter import StepMoter
from pico.CoreInfo import CoreInfo
from jengatable.JengaTableController import JengaTableController
from jengatable.JengaTable import JengaTable

# GPIO定義
P_MODE_SW = 16               # モード切替スイッチ（GPIO.IN, PULL_DOWN）
P_READ_SW = 17               # リロード起動スイッチ（GPIO.IN, PULL_DOWN）
P_STEP_MT = [10, 11, 12, 13] # エレベーター用ステップモーター（I2C）
P_TURN_SV = 1                # ターンテーブル用サーボ（I2C）
P_PUSH_SV = 0                # 押し出し機用サーボ（I2C）
P_EXEC_LT = 18               # 動作中LED（GPIO。OUT）

# スイッチセットアップ
reload_switch_counter = 0
reload_switch = Pin(P_READ_SW, Pin.IN, Pin.PULL_DOWN)
mode_switch = Pin(P_MODE_SW, Pin.IN, Pin.PULL_DOWN)

# ジェンガテーブルセットアップ
jenga_table = JengaTable()
jenga_table.setPushServo(Servo(P_PUSH_SV))
jenga_table.setTurnTableServo(Servo(P_TURN_SV))
jenga_table.setElevetorStepMotor(StepMoter(P_STEP_MT[0], P_STEP_MT[1], P_STEP_MT[2], P_STEP_MT[3]))
jenga_table.setExecLed(Led(P_EXEC_LT))

# コントローラーセットアップ
table_controller = JengaTableController(2, 1, 0)
coreInfo = CoreInfo()

print("セットアップ完了")

while True:
# メインループ:start
    if mode_switch.value() == 1:
        # マニュアルモードスイッチON
        v_elv = table_controller.getVolumeElevetor()
        if v_elv < 50:
            v_elv = -10
        elif v_elv > 130:
            v_elv = 10
        else:
            v_elv = 0
        v_turn = table_controller.getVolumeTurntable()
        v_push = table_controller.getVolumePusher()
        print("マニュアルモード|E:{0}, T:{1}, P:{2}".format(str(v_elv), str(v_turn), str(v_push)))
        jenga_table.elevatorMove(v_elv)
        jenga_table.tableTurn(v_turn)
        jenga_table.pushMove(v_push)
    else:
        # マニュアルモードスイッチOFF
        print("待機モード|S:{0}".format(reload_switch_counter))
        if reload_switch.value() == 1:
            reload_switch_counter += 1
        else:
            reload_switch_counter = 0
        if reload_switch_counter > 2:
            jenga_table.reload()

    # 情報表示
    print("電圧:{0}|コア温度:{1}".format(coreInfo.getVoltage(), coreInfo.getTemperature()))
    utime.sleep_ms(1000)
# メインループ:end
