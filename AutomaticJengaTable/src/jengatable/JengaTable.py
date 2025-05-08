import utime
from pico import Servo, StepMoterNEMA17

# ジェンガテーブルクラス
class JengaTable:
    """ジェンガテーブルクラス

        ステッピングモーター1個とサーボ2個で構成する全自動ジェンガテーブルを制御する。
        * setPushServoで押し出し機用サーボと角度範囲を登録
        * setTurnTableServoでターンテーブル用サーボと角度範囲を登録
        * setElevetorStepMotorでエレベーター用ステッピングモーターと1cms下げるのに必要なステップ数を登録
        * setStageCountでジェンガの段数を登録
    """

    _WAIT_MS_PUSH = 600   
    """待機ミリ秒_押し出し機"""

    _WAIT_MS_TURN = 1000
    """待機ミリ秒_ターンテーブル"""


    # ==================
    # セットアップ
    # ==================
    def __init__(self):
        """コンストラクタ"""
        self._is_table_turned = False
        self._has_lcd = False

    def setPushServo(self, servo:Servo, st_angle:float, ed_angle:float):
        """押出機用サーボを登録
        Args:
            servo: サーボ
            st_angle: 引き込み時角度(0.0 <= angle <= 180.0)
            ed_angle: 押し出し時角度(0.0 <= angle <= 180.0)
        """
        self._p_servo = servo
        self._p_servo.turn(st_angle)
        self._p_servo_st_angle = st_angle
        self._p_servo_ed_angle = ed_angle
    
    def setTurnTableServo(self, servo:Servo, st_angle:float, ed_angle:float):
        """ターンテーブル用サーボを登録
        Args:
            servo: サーボ
            st_angle: 元位置角度(0.0 <= angle <= 180.0)
            ed_angle: 回転時角度(0.0 <= angle <= 180.0)
        """
        self._t_servo = servo
        self._t_servo.turn(st_angle)
        self._t_servo_st_angle = st_angle
        self._t_servo_ed_angle = ed_angle

    def setElevetorStepMotor(self, stepmotor:StepMoterNEMA17, step_cnt_by_1cmdown:int):
        """エレベーター用ステッピングモーターを登録
        Args:
            stepmotor: ステッピングモーター
            step_cnt_by_1cm: 1cm移動させるためのステップ数
        """
        self._e_stepmotor = stepmotor
        # テーブル上面と装填開始位置の差は2.7cm
        self._elv_init_down_step = int(2.7 * step_cnt_by_1cmdown)
        # ジェンガ1段は1.3cm
        self._elv_stage_down_step = int(1.3 * step_cnt_by_1cmdown)

    def setStageCount(self, stage_count:int):
        """ジェンガの段数を登録
        Args:
            stage_count: ジェンガの段数
        """
        self._elv_stage = stage_count

    def setLcdMonitor(self, lcd_monitor):
        """稼働状況モニターLCDを登録
        Args:
            lcd_monitor: LCD(1802)
        """
        self._exec_monitor = lcd_monitor
        self._has_lcd = False

    # ==================
    # 装填機
    # ==================
    def _push(self):
        """ジェンガを1個押し出し"""
        self._p_servo.turn(self._p_servo_ed_angle)
        utime.sleep_ms(self._WAIT_MS_PUSH)
        self._p_servo.turn(self._p_servo_st_angle)
        utime.sleep_ms(self._WAIT_MS_PUSH)

    # ==================
    # ターンテーブル
    # ==================
    def _tableTurn(self):
        """ターンテーブルの向きを変更"""
        if self._is_table_turned:
            self._is_table_turned = False
            self._t_servo.turn(self._t_servo_st_angle)
            print("縦へ")
        else:
            self._is_table_turned = True
            self._t_servo.turn(self._t_servo_ed_angle)
            print("横へ")
        utime.sleep_ms(self._WAIT_MS_TURN)

    # ==================
    # エレベーター
    # ==================
    def _elv_init_down(self):
        """エレベーターをゲーム位置から装填開始位置へ移動"""
        print("初期位置へ移動開始")
        self._e_stepmotor.step(self._elv_init_down_step)
        print("初期位置へ移動完了")

    def _elv_stage_down(self):
        """エレベーターを1段分下降"""
        print("1段降下開始")
        self._e_stepmotor.step(self._elv_stage_down_step)
        print("1段降下完了")
        
    def _elv_fullup(self):
        """エレベーターをゲーム位置まで上昇"""
        total_down_step = self._elv_init_down_step + self._elv_stage_down_step * (self._elv_stage - 1)
        upstep = total_down_step * -1
        print("完成品上昇開始（{0}step）".format(upstep))
        self._e_stepmotor.step(upstep)
        print("完成品上昇完了")

    # ==================
    # 状態出力
    # ==================
    def infoStart(self):
        """組み立て開始"""
        print("reload start")

    def infoBuilding(self, stage_cnt:int, push_cnt:int):
        """組み立て中
        Args:
            stage_cnt: 組み立て中の段数
            push_cnt: 押し出し中の個数
        """
        print("lv_cnt:{0} push_cnt:{1}".format(stage_cnt, push_cnt))

    def infoEnd(self):
        """組み立て終了"""
        print("reload end")

    # ==================
    # ジェンガ組み立て処理
    # ==================
    def reload(self):
        """ジェンガ組み立て処理"""
        self.infoStart()
        # 押し出し機を引く -> 組み立て開始位置へ下降 -> テーブルを初期位置に回転
        self._p_servo.turn(self._p_servo_st_angle)
        utime.sleep_ms(500)
        self._elv_init_down()
        utime.sleep_ms(500)
        self._t_servo.turn(self._t_servo_st_angle)
        self._is_table_turned = False
        utime.sleep_ms(500)
        # 組み立て処理
        for lv_cnt in range(self._elv_stage):
            #print("lv_cnt:" + str(lv_cnt))
            # テーブルを回転
            self._tableTurn()
            # ジェンガを3個装填
            for p_cnt in range(3):
                self._push()
                #print("pushcnt:" + str(p_cnt))
                self.infoBuilding(lv_cnt, p_cnt)
            # 1段下げ
            if(lv_cnt < self._elv_stage -1):
                self._elv_stage_down()
        # 完成品を上昇
        self._elv_fullup()
        # 組み立て完了
        self.infoEnd()

    def demoReload(self):
        print("demo start")
        # 開始位置へ下降
        self._elv_init_down()
        # テーブルの向き変更
        self._e_stepmotor.step(-200)
        self._tableTurn()
        self._e_stepmotor.step(200)
        # ジェンガを3個装填
        for p_cnt in range(3):
            self._push()
            print("pushcnt:" + str(p_cnt))
        # テーブルの向き変更+1段下げ
        self._e_stepmotor.step(-200)
        self._tableTurn()
        self._e_stepmotor.step(200)
        self._elv_stage_down()
        # ジェンガを3個装填
        for p_cnt in range(3):
            self._push()
            print("pushcnt:" + str(p_cnt))
        # 完成品を上昇
        self._elv_stage = 2
        self._elv_fullup()
        print("demo_end")
        