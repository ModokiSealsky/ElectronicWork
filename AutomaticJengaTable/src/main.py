import utime
from pico import Led, Servo, ToggleSwitch, CoreInfo, StepMoterNEMA17
from jengatable import JengaTable, JengaTableController
from lib import LCD1602

# GPIO定義
# -------------------------------------------------------------------
P_SW_MODE = 16            # モード切替スイッチ（GPIO.IN, PULL_DOWN）
P_SW_READ = 17            # リロード起動スイッチ（GPIO.IN, PULL_DOWN）
P_MT_STEP = [12, 11, 10]  # エレベーター用ステップモーター（GPIO.OUT）
P_MT_BASE = 13            # ステップモーター用基準電圧ピン
P_SV_TURN = 3             # ターンテーブル用サーボ（I2C）
P_SV_PUSH = 2             # 押し出し機用サーボ（I2C）
P_LT_CLBT = 18            # 調整中LED（GPIO。OUT）
P_LT_WAIT = 19            # 待機中LED（GPIO。OUT）
P_LT_MARK = 20            # 準備中LED（GPIO。OUT）
P_LT_EXEC = 21            # 動作中LED（GPIO。OUT）
P_ADC_ELV = 2             # エレベーター操作用アナログ入力
P_ADC_T_S = 1             # ターンテーブル操作用アナログ入力
P_ADC_P_S = 0             # 押し出し機操作用アナログ入力
P_LCD_SDA = 14            # LCD用LDA
P_LCD_SDL = 15            # LCD用LDL
C_LCD_I2C = 1             # LCD用I2Cチャネル
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
e_motor.setBaseVolPin(P_MT_BASE)
# -------------------------------------------------------------------

# 表示系セットアップ
# -------------------------------------------------------------------
led_clbt = Led(P_LT_CLBT)
led_wait = Led(P_LT_WAIT)
led_mark = Led(P_LT_MARK)
led_exec = Led(P_LT_EXEC)
coreInfo = CoreInfo()
lcd = LCD1602(C_LCD_I2C, P_LCD_SDA, P_LCD_SDL)
lcd.display_enable(False)
lcd.display_clear()
lcd.entry_mode_set(1,0)
lcd.display_enable(True)
lcd.display_clear()
def outputInfo(ctrl_mode:bool, coreinfo:CoreInfo):
    lcd.display_clear()
    if ctrl_mode:
        lcd.print_line(1, "CTRL")
    else:
        lcd.print_line(1, "WAIT")
    lcd.print_line(2, "v:{0} t:{1}".format(coreInfo.getVoltage(), coreInfo.getTemperature()))
# -------------------------------------------------------------------

# ジェンガテーブルセットアップ
# -------------------------------------------------------------------
jenga_table = JengaTable()
jenga_table.setPushServo(p_servo, 178.0, 60.0)
jenga_table.setTurnTableServo(t_servo, 5.0, 95.0)
jenga_table.setElevetorStepMotor(e_motor, 500)
jenga_table.setStageCount(2)
jenga_table.setLcdMonitor(lcd)
# -------------------------------------------------------------------

# コントローラーセットアップ
# -------------------------------------------------------------------
table_controller = JengaTableController(P_ADC_ELV, P_ADC_T_S, P_ADC_P_S)
table_controller.setElevetorStepMotor(e_motor)
table_controller.setPushServo(p_servo)
table_controller.setTurnServo(t_servo)
# -------------------------------------------------------------------
print("セットアップ完了")
# -------------------------------------------------------------------
while True:
# メインループ:start
    # print("mod:{0} rel:{1}".format(mode_switch.isOff(), reload_switch.isOn()))
    if mode_switch.isOn():
        # 調整モード
        led_clbt.on()
        led_wait.off()
        led_mark.off()
        table_controller.move()
        # TODO
        # ボタンでサーボの初期位置変更を可能とする
        # 3路でどちらかのサーボの選択（中立は現在値表示）
        # 2路で開始か終了かの選択
    else:
        # 待機モード
        led_clbt.off()
        led_wait.on()
        print("待機モード|S:{0}".format(reload_switch_counter))
        if reload_switch.isOn():
            reload_switch_counter += 1
            led_mark.on()
        else:
            reload_switch_counter = 0
            led_mark.off()
        if reload_switch_counter > 4:
            # 2秒以上長押しで実行
            led_exec.on()
            jenga_table.reload()
            reload_switch_counter = 0
            led_mark.off()
            led_exec.off()
    # 情報表示
    print("電圧:{0}|コア温度:{1}".format(coreInfo.getVoltage(), coreInfo.getTemperature()))
    outputInfo(mode_switch.isOn(), coreInfo)
    utime.sleep_ms(500)
# メインループ:end
# -------------------------------------------------------------------
