# Pico用基礎クラスパッケージ

## 概要

電子パーツ用クラスを作成し、今後の作品で再利用できるようにする。

## 運用方針

各作品でクラスを利用する場合は必要なモノを各プロジェクトにコピーして使う。
\_\_init\_\_.pyのみ、各プロジェクト側で作成してコミットする。
クラスの追加や修正はこのパッケージへマージする。

## クラス一覧

```mermaid
classDiagram

namespace picolib {
    class Buzzer{
        init(gpio_pin_no:int)
        beep(ms:int=100)
    }

    class PwmBuzzer{
        init(pwm_pin_no:int)
        hz_beep(ms:int=100, hz:int=1000)
        play_music(music:list[Note])
    }

    class PwmBuzzer.Note {
        init(ms:int, hz:int, end_wait_ms:int = 10)
    }

    class InputSwitch{
        init(gpio_pin_no:int)
        is_on() bool
        is_off() bool
    }

    class TriggerButton{
        refresh()
        is_on_trigger() bool
        is_off_trigger() bool
    }

    class Led{
        init(gpio_pin_no:int)
        on()
        off()
    }

    class PwmMotorDriver{
        init(pin_a_no: int, pin_b_no: int, freq: int = 50)
        set_speed(speed_percent: float)
        brake()
        off()
    }

    class Servo{
        init(pwm_pin_no:int)
        set_angle(angle:float)
    }

    class StepMotor{
        <<abstract>>
        init(is_counter:bool=False, one_lap_step:int=200)
        set_counterclockwise(is_counter:bool=False)
        set_one_lap_step(step:int)
        turn_step(step:int)
        turn_angle(angle:float)
    }

    class StepMotorUnipolar{
        init()
    }

    class StepMotorBipolar{
        init()
    }
}

Buzzer <|-- PwmBuzzer
InputSwitch <|-- TriggerButton
StepMotor <|-- StepMotorUnipolar
StepMotor <|-- StepMotorBipolar

```

### Buzzer

ブザー。
指定したミリ秒数鳴らすことができる。

### PwmBuzzer

Pmw制御ブザー。
Buzzerの子クラス。
指定したミリ秒、指定した周波数を鳴らすことができる。

### InputSwitch

入力スイッチ。
onかoffかを取得できる。

### TriggerButton

トリガー検知対応ボタン。
InputSwitchの子クラス。
reflechでトリガーを更新し、onトリガーとoffトリガーを取得できる。

### Led

発光ダイオード。
点灯(on)と消灯(off)ができる。

### PwmMotorDriver

モータードライバにPWM信号を送信してDCモーターを制御する。
制御ピン2本の電位差で速度が変更できるモータードライバに対応する。
※PWMの周波数で電圧を疑似的に変化させている
正転と逆転が期待と異なる場合は配線を逆にして対応すること。

### Servo

Pwm制御のサーボ。
角度を°で指定できる。

### StepMotor

ステッピングモーター。
指定ステップ数回転、指定角度回転ができる。
指定角度回転のためには1周に必要なステップの設定が必要。
マイナス値で反時計回りの想定だが、逆回転するモーターの場合はset_counterclockwise(True)で逆回転モーターであることを指定する。

### StepMotorUnipolar

ユニポーラ制御ステッピングモーター。
StepMotorの子クラス。

### StepMotorBipolar

バイポーラ制御ステッピングモーター。
StepMotorの子クラス。

---

[戻る](../library.md)