class ScoreBord:
    """I2Cを利用するスコアボードのインターフェース"""
    def __init__(self,
                 i2c_ch: int,
                 scl_pin_no: int,
                 sda_pin_no: int):
        """初期化

            Args:
                i2c_ch: I2Cチャネル
                scl_pin_no: 使用するSCLピン番号
                sda_pin_no: 使用するSDAピン番号
        """
        print("Use Empty ScoreBord")

    def set_i2c_addr(self, addr: int):
        """ I2Cスレーブアドレス設定
        
            Args:
                addr: I2Cスレーブアドレス
        """
        print("O2C Address:{0}".format(addr))

    def display_off(self):
        """ ディスプレイ消灯 """
        print("Display Off")

    def display_check(self):
        """表示確認"""
        print("Display Check")

    def counter_start(self, start_count:int):
        """カウンター更新開始

        Args:
            start_count: ゲーム開始時カウント値
        """
        print("start_count]{0}".format(start_count))

    def counter_update(self, now_count: int):
        """カウンター値更新

        Args:
            start_count: 現在のカウント値
        """
        print("now_count]{0}".format(now_count))

    def counter_stop(self, result_count:int):
        """カウンター更新停止

        Args:
            result_count: ゲーム終了時カウント値
        """
        print("result_count]{0}".format(result_count))

    def output_count(self, count:int):
        """ゲームクリア表示"""
        print("output_count]{0}".format(count))

    def output_clear(self):
        """ゲームクリア表示"""
        print("CLEAR!!")

    def output_foul(self):
        """ゲーム失敗表示"""
        print("FOUL!!")

    def output_message(self, message: str):
        """メッセージ表示
        
        Args:
            message: 表示メッセージ
        """
        print("message:{0}".format(message))
