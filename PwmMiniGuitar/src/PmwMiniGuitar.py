import utime

from picolib import InputAdc, InputSwitch, PwmBuzzer

# ピン定義
IN_ADC = 28
"""ADC入力ピン"""
IN_N_S = 0
"""通常音ボタンピン"""
IN_H_S = 1
"""半音上ボタンピン"""
OUT_BZ = 2
"""ブザー出力ピン"""

# 処理頻度定数
FLIP_MS = 10
BASE_HZ = 440  # ラ
H_UP_RT = 13 / 12  # 半音上の比率
MAX_RT = 3  # 4オクターブ幅

# 初期化
input_adc = InputAdc(IN_ADC)
input_n_s = InputSwitch(IN_N_S)
input_h_s = InputSwitch(IN_H_S)
buzzer = PwmBuzzer(OUT_BZ)


# 周波数算出
def calc_hz(input_percent: float):
    return int(BASE_HZ + BASE_HZ * MAX_RT * input_percent / 100)


def calc_halfup_hz(input_percent: float):
    return int(BASE_HZ + BASE_HZ * MAX_RT * input_percent * H_UP_RT / 100)


# 演奏処理ループ
while True:
    adc_percent_val = input_adc.get_parcents_value()
    if input_n_s.is_on():
        buzzer.set_hz(calc_hz(adc_percent_val))
    elif input_h_s.is_on():
        buzzer.set_hz(calc_halfup_hz(adc_percent_val))
    else:
        buzzer.off()
    utime.sleep_ms(FLIP_MS)
