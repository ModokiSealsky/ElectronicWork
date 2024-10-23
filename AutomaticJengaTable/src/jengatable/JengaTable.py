import utime

# ジェンガテーブルクラス
class JengaTable:
    # ==================
    # セットアップ
    # ==================
    def __init__(self):
        """初期化
        """
        self._is_table_turned = False
        self._push_wait_ms = 1000
        self._turn_wait_ms = 1000
        self._elv_init_down_step = -500
        self._elv_stage_down_step = -200
        self._elv_stage = 3
        self._p_servo_st_angle = 0
        self._p_servo_ed_angle = 180
        self._t_servo_st_angle = 0
        self._t_servo_ed_angle = 180

    def setPushServo(self, servo):
        """押出機用サーボを登録
        """
        self._p_servo = servo
        self._p_servo.turn(0)
    
    def setTurnTableServo(self, servo):
        """ターンテーブル用サーボを登録
        """
        self._t_servo = servo
        self._t_servo.turn(0)

    def setElevetorStepMotor(self, stepmotor):
        """エレベーター用ステッピングモーターを登録
        """
        self._e_stepmotor = stepmotor

    def setExecLed(self, led):
        """稼働中表示LEDを登録
        """
        self._exec_led = led
        self._exec_led.off()

    def setExecLcdMonitor(self, lcdmonitor):
        """稼働状況モニターLCDを登録
        """
        self._exec_monitor

    # ==================
    # 装填機
    # ==================
    def _push(self):
        """ジェンガを1個押し出し
        """
        self._t_servo.turn(180)
        utime.sleep_ms(self._push_wait_ms)
        self._t_servo.turn(0)
        utime.sleep_ms(self._push_wait_ms)

    def pushMove(self, angle):
        """押出機をを手動操作
        """
        self._t_servo.turn(angle)

    # ==================
    # ターンテーブル
    # ==================
    def _tableTurn(self):
        """ターンテーブルの向きを変更
        """
        if self._is_table_turned:
            self._is_table_turned = False
            self._t_servo.turn(0)
            print("縦へ")
        else:
            self._is_table_turned = True
            self._t_servo.turn(90)
            print("横へ")
        utime.sleep_ms(self._turn_wait_ms)

    def tableTurn(self, angle):
        """ターンテーブルをを手動操作
        """
        self._t_servo.turn(angle)

    # ==================
    # エレベーター
    # ==================
    def _elv_init_down(self):
        """エレベーターをゲーム位置から装填開始位置へ移動
        """
        print("初期位置へ移動開始")
        self._e_stepmotor.step(self._elv_init_down_step)
        print("初期位置へ移動完了")

    def _elv_stage_down(self):
        """エレベーターを1段分下降
        """
        print("1段降下開始")
        self._e_stepmotor.step(self._elv_stage_down_step)
        print("1段降下完了")
        

    def _elv_fullup(self):
        """エレベーターをゲーム位置まで上昇
        """
        total_down_step = self._elv_init_down_step + self._elv_stage_down_step * self._elv_stage
        upstep = total_down_step * -1
        print("完成品上昇開始（{}step）".format(upstep))
        self._e_stepmotor.step(upstep)
        print("完成品上昇完了")

    def elevatorMove(self, step):
        """エレベーターを手動操作
        """
        self._e_stepmotor.step(step)

    # ==================
    # ジェンガ組み立て処理
    # ==================
    def reload(self):
        """ジェンガ組み立て処理
        """
        print("reload start")
        self._exec_led.on()
        # 組み立て開始位置へ下降
        self._elv_init_down()
        # 組み立て処理
        for lv_cnt in range(self._elv_stage):
            print("lv_cnt:" + str(lv_cnt))
            # ジェンガを3個装填
            for p_cnt in range(3):
                self._push()
                print("pushcnt:" + str(p_cnt))
            # 1段下げてテーブルを回転
            self._elv_stage_down()
            self._tableTurn()
        # 完成品を上昇
        self._t_servo.turn(0)
        self._elv_fullup()
        # 組み立て完了
        self._exec_led.off()
        print("reload end")
