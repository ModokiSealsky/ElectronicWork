from machine import ADC
from pico import Servo, StepMoterNEMA17

# ジェンガテーブル駆動系操作クラス
class JengaTableController:
    def __init__(self, adc_no_elv, adc_no_turn, adc_no_push):
        """コンストラクタ
        Args:
            adc_no_elv: エレベーター操作スティック用入力
            adc_no_turn: ターンテーブル操作ボリューム用入力
            adc_no_push: 押し出し機操作ボリューム用入力
        """
        self._e = ADC(adc_no_elv)
        self._t = ADC(adc_no_turn)
        self._p = ADC(adc_no_push)
        self._vol_rate = 3.3 / 65535
        self._angle_rate = 180 / 65535

    def setElevetorStepMotor(self, stepmotor:StepMoterNEMA17):
        """エレベーター用ステッピングモーターを登録
        Args:
            stepmotor: ステッピングモーター
        """
        self._s_motor = stepmotor

    def setTurnServo(self, servo:Servo):
        """ターンテーブル用サーボを登録
        Args:
            servo: サーボ
        """
        self._t_servo = servo
    
    def setPushServo(self, servo:Servo):
        """押し出し機用サーボを登録
        Args:
            servo: サーボ
        """
        self._p_servo = servo

    def _getAngle(self, adc_u16:int):
        """角度を小数点以下1桁で取得
        Args:
            adc_u16: ADCから取得したu16値
        Returns:
            0.0から180.0の角度値
        """
        vol = adc_u16 * self._angle_rate
        # -2.7-3.3-
        if vol < 0.0:
            vol = 0.0
        if vol > 180.0:
            vol = 180.0
        return float("{:.1f}".format(vol))

    def _info(self, e_angle, t_angle, p_angle):
        """入力情報表示
        Args:
            e_angle: エレベータ用入力角度
            t_angle: ターンテーブル用入力角度
            p_angle: 押し出し機用入力角度
        """
        print("input e:{0} t:{1} p:{2}".format(e_angle, t_angle, p_angle))

    def move(self):
        """入力値に応じた角度へ動かす"""
        stick_angle = self._getAngle(self._e.read_u16())
        t_srv_angle = self._getAngle(self._t.read_u16())
        p_srv_angle = self._getAngle(self._p.read_u16())
        self._info(stick_angle, t_srv_angle, p_srv_angle)
        e_step = int((stick_angle - 90.0) / 10.0)
        if e_step < -2 or e_step > 2:
            self._s_motor.step(e_step)
        self._t_servo.turn(t_srv_angle)
        self._p_servo.turn(p_srv_angle)
