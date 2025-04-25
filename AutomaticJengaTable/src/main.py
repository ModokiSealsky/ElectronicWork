import utime
from pico import Led, Servo, ToggleSwitch, CoreInfo, StepMoterNEMA17
from jengatable import JengaTable, JengaTableController

# GPIO定義
# -------------------------------------------------------------------
P_SW_MODE = 20            # モード切替スイッチ（GPIO.IN, PULL_DOWN）
P_SW_READ = 21            # リロード起動スイッチ（GPIO.IN, PULL_DOWN）
P_MT_STEP = [10, 11, 12]  # エレベーター用ステップモーター（GPIO.OUT）
P_SV_TURN = 1             # ターンテーブル用サーボ（I2C）
P_SV_PUSH = 0             # 押し出し機用サーボ（I2C）
P_LT_CLBT = 14            # 調整中LED（GPIO。OUT）
P_LT_WAIT = 15            # 待機中LED（GPIO。OUT）
P_LT_EXEC = 16            # 動作中LED（GPIO。OUT）
P_ADC_ELV = 2             # エレベーター操作用アナログ入力
P_ADC_T_S = 1             # ターンテーブル操作用アナログ入力
P_ADC_P_S = 0             # 押し出し機操作用アナログ入力
# -------------------------------------------------------------------

# スイッチセットアップ
# -------------------------------------------------------------------
reload_switch_counter = 0
reload_switch = ToggleSwitch(P_SW_READ)
mode_switch = ToggleSwitch(P_SW_MODE)
# -------------------------------------------------------------------

# 駆動系セットアップ
# -------------------------------------------------------------------
p_servo = Servo(P_SV_PUSH)
t_servo = Servo(P_SV_TURN)
e_motor = StepMoterNEMA17(P_MT_STEP[0], P_MT_STEP[1], P_MT_STEP[2])
# -------------------------------------------------------------------

# 表示系セットアップ
# -------------------------------------------------------------------
exec_led = Led(P_LT_EXEC)
coreInfo = CoreInfo()
exec_led.off()
# -------------------------------------------------------------------

# ジェンガテーブルセットアップ
# -------------------------------------------------------------------
jenga_table = JengaTable()
jenga_table.setPushServo(p_servo, 30.0, 100.0)
jenga_table.setTurnTableServo(t_servo, 3.0, 153.0)
jenga_table.setElevetorStepMotor(e_motor, 100)
jenga_table.setStageCount(2)
# -------------------------------------------------------------------

# コントローラーセットアップ
# -------------------------------------------------------------------
table_controller = JengaTableController(2, 1, 0)
table_controller.setElevetorStepMotor(e_motor)
table_controller.setPushServo(p_servo)
table_controller.setTurnServo(t_servo)
# -------------------------------------------------------------------
print("セットアップ完了")
#jenga_table.demoReload()
# -------------------------------------------------------------------
while True:
# メインループ:start
    print("mod:{0} rel:{1}".format(mode_switch.isOff(), reload_switch.isOn()))
    if mode_switch.isOn():
        # 調整モード
        table_controller.move()
        # TODO
        # ボタンでサーボの初期位置変更を可能とする
        # 3路でどちらかのサーボの選択（中立は現在値表示）
        # 2路で開始か終了かの選択
    else:
        # 待機モード
        print("待機モード|S:{0}".format(reload_switch_counter))
        if reload_switch.isOn():
            reload_switch_counter += 1
        else:
            reload_switch_counter = 0
        if reload_switch_counter > 2:
            # 2秒以上長押しで実行
            exec_led.on()
            jenga_table.reload()
            reload_switch_counter = 0
            exec_led.off()
    # 情報表示
    print("電圧:{0}|コア温度:{1}".format(coreInfo.getVoltage(), coreInfo.getTemperature()))
    utime.sleep_ms(1000)
# メインループ:end
# -------------------------------------------------------------------
